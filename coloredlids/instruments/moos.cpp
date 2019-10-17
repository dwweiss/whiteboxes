/*
  Copyright (c) 2016- by Dietmar W Weiss

  This is free software; you can redistribute it and/or modify it
  under the terms of the GNU Lesser General Public License as
  published by the Free Software Foundation; either version 3.0 of
  the License, or (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this software; if not, write to the Free
  Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
  02110-1301 USA, or see the FSF site: http://www.fsf.org.

  Version:
      2019-10-17 DWW
*/


#define HAVE_SEABREEZE

// enable HAVE_PLOT_SPECTROGRAPHS for plotting with python script
#undef HAVE_PLOT_SPECTROGRAPHS

#ifdef HAVE_PLOT_SPECTROGRAPHS
    #define PLOT_SCRIPT "/home/pi/projects/moos/plot/plot_spectra.py"
#endif
 
#include <cassert>
#include <chrono>
#include <climits>
#include <cstdio>
#include <cstdarg>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <time.h>
#include <thread>
#include <unistd.h>
#include <vector>

#include "text_diagram.h"

#ifdef HAVE_SEABREEZE
#include "api/DllDecl.h"
#include "api/SeaBreezeWrapper.h"
#endif

using namespace std;


/*   __  __   ___    ___    ____
*  |  \/  | / _ \  / _ \  / ___|
*  | |\/| || | | || | | | \___ \
*  | |  | || |_| || |_| | ___) | 
*  |_|  |_| \___/  \___/ |____/
*
*  Multiple Ocean Optics Spectrometers  rev 10.19
* 
*  Purpose:  
*    - Reads spectra from multiple Ocean Optics spectrometers
*    - Reads and stores optionally background and reference spectra
*    - Calculates transmission from actual, reference and background 
*      spectra  
*    - Plots spectra via a python script
* 
*  Version:
*      2019-10-15 DWW
* 
*  Notes:
*      On Raspberry Pi without internet, update system date manually before 
*      execution:
*          $ sudo date --set "2019-12-31 23:45"
* 
*      See constructor Meter(argc, argv) for commandline options  
*
*      The SeaBreeze library uses the term 'formatted spectrum' for the actual 
)      intensity spectrum
*/


/* 
* Averages a vector
*/ 
bool average_vector(vector<double> & X, unsigned boxcar = 0)
{    
    if (X.empty() || boxcar <= 0)
        return false;
    
    // center part 
    unsigned i, n = X.size();
 
    for (i = boxcar; i < n - boxcar; i++)
    {
        double average = X[i];
        for (unsigned j = 1; j <= boxcar; j++)
            average += X[i+j] + X[i-j];
        average /= 1 + 2 * boxcar;
        X[i] = average;
    }
    
    // left end
    double average = 0.0;
    for (i = 0; i < boxcar; i++)
        average += X[i];
    average /= boxcar;
    for (i = 0; i < boxcar; i++)
        X[i] = average;

    // right end
    average = 0.0;
    for (i = n - boxcar; i < n; i++)
        average += X[i];
    average /= boxcar;
    for (i = n - boxcar; i < n; i++)
        X[i] = average;

    return true;
}


/* 
* Formats current date and time to string
*/
string date_to_string(string format = "%Y-%m-%dT%H.%M.%S")
{
    time_t raw;
    time(&raw);
    struct tm * timeinfo = localtime(&raw);
    char buffer[256];
    strftime(buffer, sizeof(buffer), format.c_str(), timeinfo);
    return string(buffer);
}


/* 
* Splits string to array of substrings
*/
vector<string> split_string(string s, char delimiter)
{
    vector<string> array;
    int i = 0, j = 0;
    while (i < (int) s.size())
    {
        j = s.find(delimiter, i);
        string sub;
        if (j == -1)
            sub = s.substr(i);
        else
            sub = s.substr(i, j-i);
        i = j + 1;
        array.push_back(sub);
        if (j == -1)
            break;
    }

    return array;
}


/* 
* Joins array of strings
*/
string join_strings(vector<string> & array, string delimiter = "")
{
    string result;
    for (auto & el: array)
        result += el + delimiter;

    return result;
}


/*
* Purpose:
*      Parses and stores command line arguments of the program
*
*  Notes:
*      It is required that all options start with '--' and none of the
*      option values starts with "--"
*
*      It is accepted that an option has no value
*
*      If the string following an option starts with '--', then the
*          get_value() function returns string("")
*
*      If the option is the last command line argument, then the
*          get_value() function returns string("")
*/
class Parser
{
    protected:
        vector<string> argv;

    public:
        /*
        * Args:
        *     argc [int]:
        *         number of command line arguments incl. program name
        *
        *     argv [array of string]:
        *         command line arguments
        */
        Parser(int argc, char **argv)
        {
            read_arguments(argc, argv);
        }


        virtual ~Parser(){}


        /*
        * Args:
        *     argc [int]:
        *         number of command line arguments incl. program name
        *
        *     argv [array of string]:
        *         command line arguments
        *
        * Returns:
        *     [bool]:
        *         false if no commandline arguments passed
        */
        bool read_arguments(int argc, char **argv)
        {
            for (int i = 1; i < argc; i++)
                this->argv.push_back(argv[i]);

            return this->argv.size() > 1;
        }


        /*
        * Returns:
        *     [string]:
        *         name of this program
        */
        string program_name()
        {
            return argv[0];
        }


        /*
        * Args:
        *     option [string]:
        *         command line option inclusive leading '--'
        *
        *     alternative_option [string]:
        *         command line option inclusive leading '--'
        *
        * Returns:
        *     [int]:
        *         index of 'option' or '-1' if option not found
        */
        int get_index(string option, string alternative_option = "")
        {
            int i;
            for (i = 0; i < (int) this->argv.size(); i++)
                if (this->argv[i] == option)
                    return i;
            for (i = 0; i < (int) this->argv.size(); i++)
                if (this->argv[i] == alternative_option)
                    return i;
            return -1;
        }


        /*
        * Args:
        *     option [string]:
        *         command line option inclusive leading '--'
        *
        *     alternative_option [string]:
        *         alternative command line option inclusive leading '--'
        *
        * Returns:
        *     [bool]:
        *         true if 'option' is passed as argument
        */
        bool is_option(string option, string alternative_option = "")
        {
            return get_index(option, alternative_option) != -1;
        }


        /*
        * Args:
        *     option [string]:
        *         command line option inclusive leading '--'
        *
        *     alternative_option [string]:
        *         alternative command line option inclusive leading '--'
        *
        *  Returns:
        *     [string]:
        *         value of command line option or
        *         empty string if option not found
        */
        string get_value(string option, string alternative_option = "")
        {
            if (!is_option(option, alternative_option))
                return string();

            int i = get_index(option, alternative_option);
            if (i+1 == (int) this->argv.size())
                return string();

            string next_token = this->argv[i+1];
            if (next_token[0] == '-' && next_token[1] == '-')
                return string();

            return next_token;
        }
};


/*
* Prints error messages from seabreeze  
*/
bool check_for_error(int error)
{
    if (error)
    {
        cout << endl << "??? Error: " << error << endl;
        char buffer[256];
        #ifdef HAVE_SEABREEZE
        seabreeze_get_error_string(error, buffer, sizeof(buffer));
        #endif
        cout << buffer << endl;
        exit(1);
    }
    return true;
}
 

/*
* Single spectrometer device
*/
class Device
{
    public:
        unsigned index = UINT_MAX;
        unsigned pixels = 0;
        int error = 0;
        vector<double> wavelengths;
        vector<double> formatted_spectrum;
        vector<double> background_spectrum;
        vector<double> reference_spectrum;
        vector<double> buffer;
        vector<double> transmission;

    public:
        Device(unsigned index)
        {
            this->index = index;
        }


        virtual ~Device(){}

        /*
        * Reads length of intensity  ("y-array")
        */
        bool read_pixels(bool silent = false)
        {
            assert(index != UINT_MAX);

            #ifdef HAVE_SEABREEZE
            check_for_error(error);
            pixels = seabreeze_get_formatted_spectrum_length(index, &error);
            check_for_error(error);
            #else
            pixels = 10;                                // simulate a device
            #endif

            // Note: the device with serial number FLMN01736 returns 
            // mistakenly a length of ormatted spectrum of 2048, 
            // but delivers only 128 double values different from 0.0
            if (serial_number() == "FLMN01736")
            {
                if (!silent)
                    cout << "    !!! individual correction for device: '"
                        << serial_number() << "'" << endl;
                pixels = 128;
            }

            return true;
        }


        /*
        * Reads wavelength ("x-array") 
        */
        bool read_wavelengths()
        {
            if (wavelengths.size() != pixels)
                wavelengths.resize(pixels, 0.0);
            #ifdef HAVE_SEABREEZE
            seabreeze_get_wavelengths(index, &error, &wavelengths[0],
                pixels);
            check_for_error(error);
            #else
            for (unsigned pixel = 0; pixel < pixels; pixel++)
                wavelengths[pixel] = double(pixel);    // simulate device
            #endif // HAVE_SEABREEZE

            return true;
        }


        /*
        * Repair intensity ("y-array") for selected modules  
        */
        bool repair_false_pixels(vector<double> & buffer, bool silent = false)
        {
            // Note: the device with serial number FLMN03141 returns false
            // values for pixels with the indices 0 and 1
            if (serial_number() == "FLMS03141")
            {
                if (!silent)
                    cout << "    !!! individual correction for device: '"
                        << serial_number() << "'" << endl;
                int i_correct = 2;
                auto corr = buffer[i_correct];
                for (int i = 0; i < i_correct; i++)
                {
                    if (buffer[i] < 0.5 * corr || buffer[i] > 2 * corr)
                        buffer[i] = corr;
                }
            }
            return true;
        }


        bool read_spectrum(unsigned scans_to_average, 
            unsigned boxcar_width = 0, bool silent = false)
        {
            unsigned pixel;
            if (buffer.size() != pixels)
                buffer.resize(pixels, 0.0);
            if (formatted_spectrum.size() != pixels)
                formatted_spectrum.resize(pixels, 0.0);
            else
            {
                for (pixel = 0; pixel < pixels; pixel++)
                    formatted_spectrum[pixel] = 0.0;
            }

            for (unsigned scan = 0; scan < scans_to_average; scan++)
            {
                #ifdef HAVE_SEABREEZE
                seabreeze_get_formatted_spectrum(index, &error,
                    &buffer[0], pixels);
                check_for_error(error);
                
                repair_false_pixels(buffer, silent);                
                #else
                for (pixel = 0; pixel < pixels; pixel++)
                    buffer[pixel] = -1.0;
                #endif

                for (pixel = 0; pixel < pixels; pixel++)
                    formatted_spectrum[pixel] += buffer[pixel];
            }
            double reverse_denominator = 1.0 / scans_to_average;
            for (pixel = 0; pixel < pixels; pixel++)
                formatted_spectrum[pixel] *= reverse_denominator;

            average_vector(formatted_spectrum, boxcar_width);

            return true;
        }


        /* computes transmission from actual spectrum, background 
        * spectrum and reference spectrum
        *
        * Note: 
        *     'placeholder1' and 'placeholder2' are spare variables   
        */
        bool calc_transmission(double placeholder1 = 0.0,
                               double placeholder2 = 0.0)
        {
            assert(formatted_spectrum.size() == pixels);
            assert(background_spectrum.size() == pixels);
            assert(reference_spectrum.size() == pixels);

            vector<double> result;
            auto & raw = formatted_spectrum;
            for (unsigned pixel = 0; pixel < raw.size(); pixel++)
            {
                auto tau = (raw[pixel] - background_spectrum[pixel]) /
                    (reference_spectrum[pixel] - background_spectrum[pixel]);
                result.push_back(tau);
            }

            transmission = result;
            return true;
        }


    protected:
    
        bool save(string filename, vector<double> & values)
        {
            assert(wavelengths.size() == values.size());
            assert(wavelengths.size() == pixels);
            ofstream f(filename);
            if (!f.is_open())
            {
                cout << "??? file: " << filename << " not open" << endl;
                exit(1);
            }
            for (unsigned pixel = 0; pixel < pixels; pixel++)
                f << wavelengths[pixel] << "," 
                    << values[pixel] << endl;
            f.close();

            return true;
        }


    public:

        bool save_spectrum(string filename)
        {
            return save(filename, formatted_spectrum);
        }


        bool save_transmission(string filename)
        {
            if (transmission.empty())
                return false;

            return save(filename, transmission);
        }


        string model_name()
        {
            char buffer[255];
            int error = 1;
            #ifdef HAVE_SEABREEZE
            seabreeze_get_model(index, &error, buffer, sizeof(buffer));
            #endif
            check_for_error(error);
            if (error)
                return string("unknown");
            return string(buffer);
        }


        string serial_number()
        {
            char buffer[255];
            int error = 1;
            #ifdef HAVE_SEABREEZE
            seabreeze_get_serial_number(index, &error, buffer,
                sizeof(buffer));
            #endif
            check_for_error(error);
            if (error)
                return string("unknown");
            return string(buffer);
        }
};



/* Collects oservation from Observes of employing single or multiple 
*  spectrometer devices
*/
class Meter
{
    protected:
        const int ERROR_SUCCESS = 0;
        const unsigned MAX_DEVICES = 16;

    public:
        string path = "./";
        string identifier = "scan";

        unsigned long iterations = LONG_MAX;
        string integration_time_str = "0.0";
        vector<unsigned> integration_times_micro_seconds;
        unsigned scans_to_average = 1;
        double post_scans_sleep = 0.0;  // time of sleep after averaged scan [s]
        int boxcar_width = 1;           // neigbour pixels averaged in wave dir.
        int trigger_mode = 0;
        bool calibrate = false;
        bool plot_graphical = true;
        string date_time_last_scan = "";
        bool silent = false;

        int error = 0;

        vector<Device> devices;

    public:

        Meter(int argc, char** argv)
        {
            if (argc == 1)
            {
                cout << "Usage and options:" << endl << endl;
                cout << "moose";
                cout << " --calibrate                    or --cal  : interactive: dark+reference" << endl;
                cout << "      --identifier       STRING or --id   : for file name" << endl;
                cout << "      --path             STRING           : for file name" << endl;
                cout << "      --iterations  LONG UINT   or --it   : number of scans"  << endl;
                cout << "      --scans_to_average UINT   or --avg  : number of averaged scans" << endl;
                cout << "      --integration_time STRING(S) or --int : integration time [s]" << endl;
                cout << "      --trigger_mode     INT    or --trig : trigger mode (0, 1, 2, 3)" << endl;
                cout << "      --post_scan_sleep  DOUBLE or --post : delay between scans [s]" << endl;
                cout << "      --boxcar_width     INT    or --box  : boxcar width" << endl;
                cout << "      --silent                  or --s    : no display output" << endl;
                exit(-1);
            }

            prolog();
            initialize(argc, argv);
        }


        virtual ~Meter()
        {
        }


        bool prolog()
        {
            cout << " __  __   ___    ___   ____    " << endl;
            cout << "|  \\/  | / _ \\  / _ \\ / ___|" << endl;
            cout << "| |\\/| || | | || | | |\\___ \\" << endl;
            cout << "| |  | || |_| || |_| | ___) |" << endl;
            cout << "|_|  |_| \\___/  \\___/ |____/    ";
            cout << "Multiple Ocean Optics Spectrometers  rev 10.19a" << endl 
                << endl << endl;
            return true;
        }


        bool initialize(int argc, char** argv)
        {
            cout << "*** Options" << endl;
            Parser parser(argc, argv);
            string s;

            s = parser.get_value("--id", "--identifier");
            if (!s.empty())
                 identifier = s;
            else
                identifier = "default";
            cout << "    identifier: '" << identifier << "'" << endl;


            s = parser.get_value("--it", "--iterations");
            if (!s.empty())
                iterations = atoi(s.c_str());
            else
                iterations = 0;
            if (iterations < 1)
                iterations = LONG_MAX;
            cout << "    iterations: " << iterations;
            if (iterations == LONG_MAX)
                cout << " (infinite loop)";
            cout << endl;

            s = parser.get_value("--int", "--integration_time");
            if (!s.empty())
                 integration_time_str = s;
            else
                integration_time_str = "1e-3";
            // integration_time = max(integration_time, 1e-6);
            // integration_time = min(integration_time, 1e+2);
            cout << "    integration_time_str: '" << integration_time_str 
                << "' [s]" << endl;

            s = parser.get_value("--avg", "--scans_to_average");
            if (!s.empty())
                scans_to_average = atol(s.c_str());
            else
                scans_to_average = 1;
            cout << "    scans_to_average: " << scans_to_average;
            if (scans_to_average == 1)
                cout << " (no averaging)";
            cout << endl;

            s = parser.get_value("--post", "--post_scans_sleep");
            if (!s.empty())
                post_scans_sleep = atof(s.c_str());
            else
                post_scans_sleep = 1.0;
            cout << "    post_scans_sleep: " << post_scans_sleep << " [s]";
            if (post_scans_sleep == 0.0)
                cout << " (no post scan sleep)";
            cout << endl;

            s = parser.get_value("--path");
            if (!s.empty())
            {
                 path = s;
                 if (path.back() != '/' && path.back() != '\\')
                    path += '/';
            }
            else
                path = "./";
            cout << "    path: '" << path << "'" << endl;

            s = parser.get_value("--trig", "--trigger_mode");
            if (!s.empty())
                 trigger_mode = atoi(s.c_str());
            else
                trigger_mode = 0;
            cout << "    trigger_mode: " << trigger_mode << endl;

            s = parser.get_value("--box", "--boxcar_width");
            if (!s.empty())
                boxcar_width = atoi(s.c_str());
            else
                boxcar_width = 1;
            cout << "    boxcar_width: " << boxcar_width << endl;

            calibrate = parser.is_option("--cal", "--calibrate");
            cout << "    calibrate: " << calibrate << endl;

            silent = parser.is_option("--s", "--silent");
            cout << "    silent: " << silent << endl;

            return true;
        }
        

    protected:

        bool pre()
        {
            cout << endl << "*** Pre-processing" << endl;

            cout << "    device index(es): [ ";
            devices.clear();
            for (unsigned j = 0; j < MAX_DEVICES; j++)
            {
                #ifdef HAVE_SEABREEZE
                seabreeze_open_spectrometer(j, &error);
                #else
                error = j;                     // allow one dummy device
                #endif
                if (error)
                    break;
                auto device = Device(j);
                devices.push_back(device);
                cout << devices[j].index << ", ";
            }
            cout << "]";
            cout << ", count: " << devices.size() << endl;
            if (devices.empty())
            {
                cout << endl << "??? No devices connected" << endl;
                exit(1);
            }

            cout << "    serial_number(s): [";
            for (auto & device : devices)
                cout << device.serial_number() << " (" 
                    << device.model_name() << "), ";
            cout << "]" << endl;

            for (auto & device : devices)
                device.read_pixels(silent=silent);
            cout << "    pixels: [";
            for (auto & device : devices)
                cout << device.pixels << ", ";
            cout << "], count: " << devices.size() << endl;

            // split integration time string (delimiter ':') and convert
            // to array of integration time in micro seconds 
            vector<unsigned long> int_tim;
            vector<string> str_arr = split_string(
                integration_time_str, ':');
            if (str_arr.size() < devices.size())
            {
                unsigned n = str_arr.size();
                for (unsigned i = n; i < devices.size(); i++)
                    str_arr.push_back(str_arr[n-1]);
            }
            integration_times_micro_seconds.clear();
            for (unsigned i = 0; i < devices.size(); i++)
            {   
                double t_s = atof(str_arr[i].c_str());
                unsigned t_us = unsigned(t_s * 1e6);
                integration_times_micro_seconds.push_back(t_us);
            }
            cout << "    integration_times: [";
            for (auto x:integration_times_micro_seconds)
                cout << x << ", ";
            cout << "] [micro seconds]" << endl;

            unsigned i_dev = 0;
            for (auto & device : devices)
            {
                #ifdef HAVE_SEABREEZE
                seabreeze_set_integration_time_microsec(device.index, &error,
                    integration_times_micro_seconds[i_dev]);
                #endif
                i_dev++;
                check_for_error(error);
 
                #ifdef HAVE_SEABREEZE
                seabreeze_set_trigger_mode(device.index, &error, trigger_mode);
                #endif

                check_for_error(error);
            }

            for (auto & device : devices)
            {
                device.read_wavelengths();
                auto max = device.wavelengths[0];
                for (auto el : device.wavelengths) if (el > max) max = el;
                auto min = device.wavelengths[0];
                for (auto el : device.wavelengths) if (el < min) min = el;
                if (device.index == 0)
                    cout << "    wavelengths";
                else
                    cout << "               ";
                cout << "[" << device.index << "]";
                cout << ": ("
                    << device.wavelengths[0] << ", " << device.wavelengths[1]
                    <<  ", ..., " << device.wavelengths.back() << ")";
                if (false)
                {
                    // TODO remove min, max and count after release test
                    cout << ", min: " << min << ", max: " << max
                         << ", count: " << device.wavelengths.size();
                }
                cout << endl;
            }

            if (calibrate)
            {
                cout << endl << "*** Manual calibration" << endl;
                cout << "    (see program option '--calibration' for details)" 
                    << endl;


                cout << endl << "+++ Read reference spectrum" << endl;
                cout << "    ==> required action: light source ON, "
                    << "EMPTY fluid cell"  << endl;
                cout << "    if ready, press [enter]";
                cin.get();
                for (auto & device : devices)
                {
                    string filename = path + identifier 
                        + "_reference_spectrum_device"
                        + to_string(device.index) + ".data";
                    device.read_spectrum(scans_to_average, boxcar_width, silent);
                    device.reference_spectrum = device.formatted_spectrum;
                    if (device.save_spectrum(filename))
                        cout << "    Reference spectrum saved as: " 
                            << filename << endl;
                    TextDiagram(string("reference") + to_string(device.index), 
                        device.wavelengths, device.reference_spectrum);
                }

                cout << "+++ Read dark spectrum" << endl;
                cout << "    required action ==> light source OFF, "
                    << "EMPTY cuvette/flow cell" << endl;
                cout << "    if ready, press [enter] ";
                cin.get();
                for (auto & device : devices)
                {
                    string filename = path + identifier + 
                        "_background_spectrum_device" 
                        + to_string(device.index) + ".data";
                    device.read_spectrum(scans_to_average, boxcar_width, silent);
                    device.background_spectrum = device.formatted_spectrum;
                    if (device.save_spectrum(filename))
                        cout << "    Background spectrum saved as: " << filename 
                            << endl;
                    TextDiagram(string("background") + to_string(device.index), 
                        device.wavelengths, device.background_spectrum);
                }

                cout << endl << "+++ Read spectrum of actual fluid" << endl;
                cout << "    ==> required action: light source ON, " 
                    << "FILL cuvette/fluid cell" << endl;
                cout << "    if ready, press [enter]";
                cin.get();
            }
            cout << endl;

            return true;
        }


        double task()
        {
            cout << "*** Task (iterations: " << iterations << ")" << endl;

            for (long unsigned it = 0; it < iterations; it++)
            {
                string date_time = date_to_string();
                this->date_time_last_scan = date_time; 
                string tim = date_time.substr(11); tim[2] = ':'; tim[5] = ':';
                cout << "    it: " << it << " (" << tim << "), device(s): [";
                string filebasename = path + identifier + "_" + date_time;

                for (auto & device : devices)
                {
                    cout << device.index << ", ";

                    device.read_spectrum(scans_to_average, boxcar_width, 
                        silent);

                    device.save_spectrum(filebasename 
                        + "_spectrum_device"
                        + to_string(device.index) + ".data");
                    if (!device.reference_spectrum.empty())
                    {
                        device.calc_transmission();
                        device.save_transmission(filebasename + 
                            "_transmission_device" + 
                            to_string(device.index) + ".data");
                        TextDiagram(string("transmission_") + 
                            to_string(device.index), device.wavelengths, 
                            device.transmission, true, 0.0, 0.0, -0.1, 1.1);
                    }                        

                }
                cout << "]" << endl;

                if (post_scans_sleep > 600.0)
                    std::this_thread::sleep_for(std::chrono::minutes(
                        static_cast<unsigned long>(post_scans_sleep / 60)));
                else if (post_scans_sleep > 10.0)
                    std::this_thread::sleep_for(std::chrono::seconds(
                        static_cast<unsigned long>(post_scans_sleep * 1)));
                else
                    std::this_thread::sleep_for(std::chrono::milliseconds(
                        static_cast<unsigned long>(
                            post_scans_sleep * 1e3)));
                #if 0
                auto delay = static_cast<unsigned long long>(
                    post_scans_sleep * 1e6);
                usleep(delay);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
                #endif
            }
            return 0.0;
        }


        bool post()
        {
            cout << endl << "*** Post-processing" << endl;
            cout << "    close device(s): [";

            for (auto & device : devices)
            {
                cout << device.index << ", ";
                #ifdef HAVE_SEABREEZE
                seabreeze_close_spectrometer(device.index, &error);
                #endif
                check_for_error(error);
            }
            cout << "]" << endl;
            
            
            #ifdef HAVE_PLOT_SPECTROGRAPHS
            cout << "+++ plot" << endl;
            
            string command = "python3 ";
            command += PLOT_SCRIPT;
            command += " " + this->path + " " + this->identifier + " " +
                this->date_time_last_scan;
            system(command.c_str());
            #endif 

            return true;
        }


    public:

        double run()
        {
            pre();
            double res = task();
            post();
            return res;
        }
};


int main(int argc, char **argv)
{
    Meter foo(argc, argv);
    foo.run();
    return 0;
}
