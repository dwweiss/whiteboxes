"""
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
      2019-11-19 DWW
"""

__all__ = ['plot_spectra']

import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from nptyping import Array
from typing import List, Tuple


def plot_spectra(path: str, 
                 identifier: str, 
                 date_time: str, 
                 skip: int = 0, 
                 delimiter: str = ',',
                 save_image: bool = False) -> bool:
    """
    Plots optical spectra (x, y(x)) stored in set of 8 CSV files with 
        background       spectra for device0 and device1
        reference        spectra for device0 and device1
        actual intensity spectra for device0 and device1
        transmission             for device0 and device1
    see _generate_filename_set() fro the definition of the file names. 

    Each data file contains two columns with floating point numbers:
        
        # optional header lines 
        1.2, 3.4
        5.6, 7.8
          ...
        9.0, 1.2

    Args:
        path:
            path to file

        identifier:
            identifier of set of data files comprising:
                background, reference, intensity, and transmission 
                spectra files
            
        date_time:
            date and time in the notation: '2000-12-31T23.59.59'
            
        skip:
            number of header rows to be skipped
            
        delimiter:
            delimiter between first and second column                
            
        save_image:
            if True, plots will be saved as png-file
    
    Returns:
        False if files not found        
    """
    filename_set = _generate_filename_set(identifier, date_time)    
    ok = _plot_file_set(path, identifier, date_time, skip, delimiter, 
                        save_image, *filename_set)
    return ok


def _generate_filename_set(identifier: str, date_time: str) -> List[str]:
    """
    Generates set of file names of actual intensity, background and 
    reference spectra 
    
    Args:
        identifier:
            identifier of set of data files
            
        date_time:
            date and time notation, eg: '2000-12-31T23.59.59'
    
    Returns:
        list of file names    
    """
    fb0 = identifier + '_background_spectrum_device0.data'
    fb1 = identifier + '_background_spectrum_device1.data'

    fr0 = identifier + '_reference_spectrum_device0.data'
    fr1 = identifier + '_reference_spectrum_device1.data'

    fi0 = identifier + '_' + date_time + '_spectrum_device0.data'
    fi1 = identifier + '_' + date_time + '_spectrum_device1.data'

    ft0 = identifier + '_' + date_time + '_transmission_device0.data'
    ft1 = identifier + '_' + date_time + '_transmission_device1.data'
    
    return [fb0, fb1, fr0, fr1, fi0, fi1, ft0, ft1]


def _plot_file_set(path: str, 
                   identifier: str,
                   date_time: str,
                   skip: int,
                   delimiter: str,
                   save_image: bool,
                   fb0: str, fb1: str, 
                   fr0: str, fr1: str,
                   fi0: str, fi1: str, 
                   ft0: str, ft1: str) -> bool:
    """
    Plots spectra stored in set of CSV files containing 2 float columns 

    Args:
        path:
            path to file

        identifier:
            identifier of set of data files

        date_time:
            date and time in the notation: '2000-12-31T23.59.59'
 
        skip:
            number of header rows to be skipped
            
        delimiter:
            delimiter between first and second column

        save_image:
            if True, plots will be saved as png-file

        fb0:
            file name of backgound spectrum 0

        fb1:
            file name of backgound spectrum 1
            
        fr0:
            file name of reference spectrum 0

        fr1:
            file name of reference spectrum 1

        fi0:
            file name of intensity spectrum 0

        fi1:
            file name of intensity spectrum 1

        ft0:
            file name of transmission spectrum 0

        ft1:
            file name of transmission spectrum 1     
    
    Returns:
        False if files not found        
    """
    
    plot_all_readings = False
    w0, r0 = _read_csv_two_columns(path, fr0, plot_all_readings)
    w1, r1 = _read_csv_two_columns(path, fr1, plot_all_readings)
    w0, i0 = _read_csv_two_columns(path, fi0, plot_all_readings)
    w1, i1 = _read_csv_two_columns(path, fi1, plot_all_readings)
    w0, b0 = _read_csv_two_columns(path, fb0, plot_all_readings)
    w1, b1 = _read_csv_two_columns(path, fb1, plot_all_readings)
 
    if not (len(r0) and len(i0) and len(b0)):
        return False

    plt.title('reference, spectrum and background intensity')
    plt.xlabel('wavelength [nm]')
    plt.ylabel('intensity [digits]')
    if len(w0) and len(r0) and len(w1) and len(r1):
        plt.plot(w0, r0, '--', label='ref 0')
        plt.plot(w1, r1, '--', label='ref 1')

    if len(w0) and len(i0) and len(w1) and len(i1):
        plt.plot(w0, i0, label='int 0')
        plt.plot(w1, i1, label='int 1')
     
    if len(w0) and len(b0) and len(w1) and len(b1):
        plt.plot(w0, b0, label='bck 0')
        plt.plot(w1, b1, label='bck 1')
        
    if len(b0) or len(i0) or len(r0):
        plt.legend()
        plt.grid()
        if save_image:
            plt.savefig(path + identifier + date_time + \
                        '_reference_backgound_intensity.png')
        plt.show()

    w0, t0 = _read_csv_two_columns(path, ft0, plot_all_readings)
    w1, t1 = _read_csv_two_columns(path, ft1, plot_all_readings)
    if not len(t0) or not len(t1):
        
        print('shape:', i0.shape, i1.shape, 
              b0.shape, b1.shape, 
              r0.shape, r1.shape, )
        
        t0 = (i0 - b0) / (r0 - b0)
        t1 = (i1 - b1) / (r1 - b1)
        
    plt.title('transmission (' + identifier + ') ' + date_time)
    y_limits = ([0, 1], [-0.1, 1.1], ) 
    plt.ylim(y_limits[1])
    t0 = np.asfarray(t0)
    t1 = np.asfarray(t1)
    plt.ylim([-0.1, 1.1])
    plt.xlabel('wavelength [nm]')
    plt.ylabel('transmission [/]')
    plt.plot(w0, t0, label='device 0')
    plt.plot(w1, t1, label='device 1')
    plt.legend()
    plt.grid()
    if save_image:
        plt.savefig(path + identifier + date_time + '_transmission.png')
    plt.show()


def _read_csv_two_columns(path: str, 
                          file: str, 
                          skip: int = 0,
                          delimiter: str = ',',
                          plot: bool = True) \
        -> Tuple[Array[float], Array[float]]:
    """
    Reads two colums with floating point numbers from comma separated file
    
        # optional header lines 
        1.2, 3.4
        5.6, 7.8
          ...
        9.0, 1.2

    Args:
        path:
            path to file

        file:
            file name incl. extension
            
        skip:
            number of header rows to be skipped
            
        delimiter:
            delimiter between first and second column
            
        plot:
            if True, loaded data will be plotted
            
    Returns:
        X and Y as 1D arrays 
        The returned arrays are empty if file not found
    """
    path.replace('\\', '/')
    full_path = os.path.join(path, file)
    X, Y = [], []
    if os.path.isfile(full_path):
        with open(full_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for i_skip in range(skip):
                next(reader)
            for row in reader:
                X.append(float(row[0]))
                Y.append(float(row[1]))
        csv_file.close()
        if plot:
            print('+++ plot:', full_path)
            plt.plot(X, Y)
            plt.show()
    else:
        print('??? file not found:', full_path)
        
    return np.asfarray(X), np.asfarray(Y)
