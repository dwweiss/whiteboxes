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
      2019-11-07 DWW
"""

from collections import OrderedDict
from datetime import datetime
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.axes._subplots import Axes
import tkinter
from tkinter import filedialog
from typing import Any, Callable, Dict, List, Optional, Tuple


class GuiBase1():
    """
    Example of graphic user interface for calling a simulation
    
    - Interface is based on tkinter + matplotlib
    - Calls a model(data, canvas, subplot) and plots results during 
          simulation
    
    
    Organization of frames and widgets (self.root_window is root)
        
    ----------------------------------------- - - -
    |  self.root_window
    |
    |
    |   ----------------------------------------------------------------
    |   |  frm_top                                                     |
    |   ----------------------------------------------------------------                                                                
    :   ----------------------------------------------------------------
    :   |  frm_center                                                  | 
    :   |                                                              |
        |  -----------------------------   --------------------------  |
        |  |  frm_plot                 |   |   frm_param            |  |
        |  |                           |   |                        |  |
        |  |  ----------------------   |   |   [buttons]            |  |
        |  |  |                    |   |   |   [sliders]            |  |
        |  |  |   cnv_plot         |   |   |   [spin boxes]         |  |
        |  |  |                    |   |   |   [radio buttons]      |  |
        |  |  |                    |   |   |                        |  |
        |  |  ----------------------   |   |       ...              |  |
        |  |                           |   |                        |  |
        |  -----------------------------   --------------------------  |
        ----------------------------------------------------------------
        ----------------------------------------------------------------
        |  frm_bottom                                                  |
        |                                   [simulate] ... [quit]      |
        ----------------------------------------------------------------
    """

    def __init__(self, 
                 identifier: str='Simulate', 
                 model: Optional[Callable]=None,
                 labels: List[str]=['x', 'y1', 'y2'],
                 param_list: Optional[Tuple[Tuple[str, List]]]=None,
                 about_text: Optional[str]=None,
                 help_text: Optional[str]=None,                 
                ) -> None:
        """
        Args 
            identifier
                identifier of simulation
                
            model
                implementation of user-defined model 
                  model(data: Dict[str, Any], 
                        canvas: FigureCanvasTkAgg, 
                        axes: List[Axes]) 
                employed in self.simulation()
            
            labels 
                list of axis labels: [x_label, y1_label, y2_label, ...]
                
                Note: length of label list defines number of 
                      subplots, n_subplots = len(labels)-1
        
            param_list:
                List of widget descriptions 
                (
                 (type, [par_name, par_min, par_max, default], [...], ),
                 (type, [par_name, par_min, par_max, default], [...], ),
                )
                
                'type' is 'spin', 'slider', 'entry', or 'check'
                'par_min', 'par_max' and 'default' are optional
                type of 'par_min','par_max','default' is str, int, float
                                
                Note: Tuples with only one member require a comma before 
                      closing parenthesis, 
                      e.g. ('name') is invalid, but ('name',) is OK
        """
        if param_list is None:
            # demo list of widgets
            param_list = (
                ('spin',   ['n1', -1, 4], ['n2']),
                ('slider', ['iterations', 0, 500, 50], ['n2'],),
                ('entry',  ['f2', None, None, '?']),
                ('slider', ['sl2', -10, 500, 50]),
                ('check',  ['silent', None, None, False], ['calibrate']),
            )
        if about_text is None:
            about_text = 'placeholder\nplaceholder\nplaceholder\n'
        if help_text is None:
            help_text = 'placeholder\nplaceholder\nplaceholder\n'

        self.identifier: str = identifier
        self.root_window: Optional[Any] = None
        self.data: Optional[Dict[str, Any]] = self.new_file()        
 
        self.widgets: Optional[Dict[str, Any]] = OrderedDict()        
        self.i_row: int = 0  # row counter in sub-frame 'frm_param'
        self.labels: List[str] = labels
        self.about_text: str = about_text
        self.help_text: str = about_text
        
        self.param_list = param_list

        self.model: Optional[Callable] = model

    def new_file(self) -> Dict[str, Any]:
        self.data = OrderedDict()
        return self.data
        
    def open_file(self) -> bool:
        name = filedialog.askopenfilename()
        self.data = json.load(open(name, 'r'))
        return True

    def save_file(self) -> bool:
        filetypes = [('Json Files', '*.json'),  
             ('Data Files', '*.data'), 
             ('All Files', '*.*')] 
        f = filedialog.asksaveasfile(filetypes = filetypes, 
                                     defaultextension='.json') 
        json.dump(self.data, open(str(f.name), 'w'), indent=4)
        return True
        
    def about(self) -> None:
        sub = tkinter.Toplevel(width=200, height=120) 
        sub.title('About') 
        sub_txt = tkinter.Text(sub, height=25, width=72) 
        sub_txt.insert(tkinter.END, self.about_text)
        sub_txt.grid(column=0, row=0)
        sub_btn = tkinter.Button(sub, text="Quit", command=self._quit)
        sub_btn.grid(column=1, row=1)

    def help_(self) -> None:
        sub = tkinter.Toplevel(width=200, height=120) 
        sub.title('Help') 
        sub_txt = tkinter.Text(sub, height=25, width=72) 
        sub_txt.insert(tkinter.END, self.help_text)
        sub_txt.grid(column=0, row=0)
        sub_btn = tkinter.Button(sub, text="Quit", command=self._quit)
        sub_btn.grid(column=1, row=1)
        
    def update_data(self, dummy=None) -> None:  # dummy is needed for Scale
        for key, value_get in self.widgets.items():
            if not isinstance(value_get, tkinter.Label):
                self.data[key] = value_get.get()
        
        now = datetime.now()
        self.data['timestamp'] = now.strftime('%Y-%m-%dT%H:%M:%S')      

        json.dump(self.data, open('./.config.json', 'w'), indent=4)
    
    def update_and_quit(self) -> None:
        self.update_data()
        self.root_window.destroy()        
        
    def simulate(self) -> float:        
        figure = Figure(figsize=(10, 6))
        canvas = FigureCanvasTkAgg(figure, master=self.frm_plot)
        canvas.get_tk_widget().grid(row=0, column=0)

        axes = figure.subplots(len(self.labels)-1, sharex=True, sharey=True)
        # title above first subplot
#        axes[0].set_title(self.identifier)
        axes[-1].set_xlabel(self.labels[0])
        for i, ax in enumerate(axes):
            ax.set_ylabel(self.labels[i+1])
            ax.grid()

        ### MODEL ###
        res = self.model(self.data, canvas, axes)

        if 'result' in self.widgets:
            self.widgets['result'].configure(text=str(res), 
                anchor='w', borderwidth=2, relief='sunken')
            if res == -1:
                self.widgets['result'].configure(background='red')
    
    def view_log(self):
        pass

    def evaluate(self) -> None:
        pass
        
    def create_menus(self) -> None:
        mainmenu = tkinter.Menu(self.root_window)
        self.root_window.config(menu=mainmenu)
        
        filemenu = tkinter.Menu(mainmenu)
        mainmenu.add_cascade(label='File', menu=filemenu)
        filemenu.add_command(label='New', command=self.new_file)
        filemenu.add_command(label='Load', command=self.open_file)
        filemenu.add_command(label='Save', command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label='Quit', command=self._quit)
        
        helpmenu = tkinter.Menu(mainmenu)
        mainmenu.add_cascade(label='Help', menu=helpmenu)
        helpmenu.add_command(label='About', command=self.about)
        helpmenu.add_command(label='Help', command=self.help_)    

    def create_frames_and_action_buttons(self) -> None:
        
        # define frames and sub-frames         
        frm_top = tkinter.Frame(self.root_window)
        frm_top.grid(column=0, row=0)
        frm_center = tkinter.Frame(self.root_window)
        frm_center.grid(column=0, row=1)
        frm_bottom = tkinter.Frame(self.root_window)
        frm_bottom.grid(column=0, row=2)
        self.frm_param = tkinter.Frame(frm_center)
        self.frm_param.grid(column=1, row=0)
        self.frm_plot = tkinter.Frame(frm_center)
        self.frm_plot.grid(column=0, row=0)

        ## create action buttons 
        btn_sim = tkinter.Button(frm_bottom, text='Simulate', 
                                 command=self.simulate)
        btn_sim.grid(column=0, row=0, padx=10, pady=10)
        
#        btn_eval = tkinter.Button(frm_bottom, text='Evaluate', 
#                                  command=self.evaluate)
#        btn_eval.grid(column=1, row=0, padx=10, pady=10)
#
#        btn_log = tkinter.Button(frm_bottom, text='Log file', 
#                                 command=self.view_log)
#        btn_log.grid(column=2, row=0, padx=10, pady=10)
    
        btn_quit = tkinter.Button(frm_bottom, text='Quit', 
                                  command=self.update_and_quit)
        btn_quit.grid(column=3, row=0, padx=10, pady=10)

        # create placeholder reserving space for plotting canvas 
        cnv_dummy = tkinter.Canvas(self.frm_plot, width=800, height=480)
        cnv_dummy.create_rectangle(0+26, 0+10, 800-30, 480-2*10, fill='white')
        cnv_dummy.grid(row=0, column=0)


    def create_parameter_input(self) -> None:
        """
        Creates widgets for parameter input in parameter frame 
        """
        
        pady = 5
        lbl_width = 15
        root = self.root_window 
        self.i_row = 0

        def create_sliders(self, keys_and_ranges):
            for key_and_range in keys_and_ranges:
                key = key_and_range[0]
                
                from_ = key_and_range[1] if len(key_and_range) > 1 else 0
                to = key_and_range[2] if len(key_and_range) > 2 else 100
                default = key_and_range[3] if len(key_and_range) > 3 \
                                           else (from_ + to) / 2
                
                self.widgets[key] = tkinter.Scale(self.frm_param, from_=from_, 
                    to=to, orient=tkinter.HORIZONTAL,
                    resolution = (to - from_) / 100, width = 8,
                    command=self.update_data)
                self.widgets[key].set(default)
    
                self.widgets[key].grid(column=0, row=self.i_row, 
                                       padx=10, pady=pady)
                tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                    anchor='w').grid(column=1, row=self.i_row, 
                                     padx=10, pady=pady)
                self.i_row += 1

        def create_spin_boxes(self, keys_and_ranges):
            for key_and_range in keys_and_ranges:
                key = key_and_range[0]
                
                from_ = key_and_range[1] if len(key_and_range) > 1 else 0
                to = key_and_range[2] if len(key_and_range) > 2 else 100
                default = key_and_range[3] if len(key_and_range) > 3 else 'abc'
                
                v = tkinter.StringVar(self.frm_param, value=str(default))
                self.widgets[key] = tkinter.Spinbox(self.frm_param, 
                    from_=from_, to=to, width=14, 
                    textvariable=v, command=self.update_data)
                self.widgets[key].grid(column=0, row=self.i_row, 
                                       padx=10, pady=pady)
                tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                    anchor='w').grid(column=1, row=self.i_row, 
                                     padx=10, pady=pady)
                self.i_row += 1

        def create_entry_forms(self, keys_and_ranges):
            for key_and_range in keys_and_ranges:
                key = key_and_range[0]
                default = key_and_range[3] if len(key_and_range) > 3 else 'abc'

                self.widgets[key] = tkinter.StringVar(self.frm_param, default)
                tkinter.Entry(self.frm_param, textvariable=self.widgets[key], 
                              width=14+2,
                    validate="focusout", 
                    validatecommand=self.update_data).grid(
                    column=0, row=self.i_row, padx=10, pady=pady)
                tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                    anchor='w').grid(column=1, row=self.i_row, padx=10, 
                                     pady=pady)        
                self.i_row += 1

        def create_check_buttons(self, keys_and_ranges):
            for key_and_range in keys_and_ranges:
                key = key_and_range[0]
                default = key_and_range[3] if len(key_and_range) > 3 else 1

                self.widgets[key] = tkinter.IntVar(root)        
                w = tkinter.Checkbutton(self.frm_param, 
                    variable=self.widgets[key],
                    onvalue = 1, offvalue = 0, anchor='e', width = 13,
                    command=self.update_data)
                w.grid(column=0, row=self.i_row, padx=0, pady=pady)
                if default:
                    w.select()
                tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                    anchor='w').grid(column=1, row=self.i_row, padx=0, 
                                     pady=pady)        
                self.i_row += 1

        def create_labels(self, keys_and_ranges):
            for key_and_range in keys_and_ranges:
                key = key_and_range[0]
                default = key_and_range[3] if len(key_and_range) > 3 else '?'

                self.widgets[key] = tkinter.Label(self.frm_param, text=default, 
                                                  width=14)
                self.widgets[key].grid(column=0, row=self.i_row, 
                            padx=10, pady=pady)
                tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                    anchor='w').grid(column=1, row=self.i_row, 
                                     padx=10, pady=pady)        
                self.i_row += 1

        call_creation_of_widget = {
            'spin':   create_spin_boxes,
            'slider': create_sliders,
            'entry':  create_entry_forms,
            'check':  create_check_buttons,
            'label':  create_labels,
        }

            
        if self.param_list:
            for par in self.param_list:
                call_creation_of_widget[par[0]](self, par[1:])
                
        if 'result' in self.widgets:
            self.widgets['result'].configure(text='?', 
                        borderwidth=2, relief='raised', anchor='w')


    def _quit(self) -> None:
        self.root_window.quit()
        self.root_window.destroy()

    def __call__(self) -> None:
        self.root_window = tkinter.Tk()
        self.root_window.title(self.identifier)
     
        self.create_menus()
        self.create_frames_and_action_buttons()        
        self.create_parameter_input()
        
        tkinter.mainloop()


#def model_a(data: Dict[str, Any], 
#            canvas: FigureCanvasTkAgg,
#            axes: List[Axes]) -> float:
#    """
#    Implements user-defined model 
#    
#    Args:
#        data:
#            parameter and results of model
#            
#        canvas:
#            plotting canvas
#            
#        axes:
#            subplot of matplotlib figure
#            
#    Returns:
#        result of analyis
#    """
#    res = 0.123456
#
#    n = int(data['time [days]'])
#    ax1, ax2 = axes
#    
#    ax1.set_xlim(0, n)   
#    ax1.set_ylim(-2, 2)
#    ax1.plot(0., 0., color='red', marker='x', linestyle='')
#    canvas.draw()
#    
#    start = time.time()
#    prev = start
#    for it in range(n):
#
#        ###############################
#        y1 = random.uniform(-1, 1)
#        y2 = random.uniform(-1, 1)
#        ###############################
#        
#        x = it+1
#        ax1.plot(x, y1, marker='o', markersize=3, color='red')
#        ax2.plot(x, y2, marker='o', markersize=3, color='blue')
#
#        now = time.time()
#        dt = now - prev
#        if dt > 2.:
#            if not data['silent']:
#                print('wall clock time:', now - start)
#            prev = now
#            canvas.draw()
#            
#        time.sleep(0.1)
#        
#    canvas.draw()
#    
#    return res
