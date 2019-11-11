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
      2019-11-11 DWW
"""

import os
import tempfile
from collections import OrderedDict
from datetime import datetime
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter
from tkinter import filedialog
from tkinter.ttk import Progressbar
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class GuiBase1():
    """
    Example of graphic user interface for calling a simulation
    
    - Interface is based on tkinter + matplotlib
    - Calls a model(data, figure) and plots results during simulation
    

    Organization of frames and widgets (self.root_window is root)
        
    ----------------------------------------- - - -
    |  self.root_window
    |
    |
    |   ----------------------------------------------------------------
    |   |  frame_top                                                   |
    |   ----------------------------------------------------------------                                                                
    :   ----------------------------------------------------------------
    :   |  frame_center                                                | 
    :   |                                                              |
        |  -----------------------------   --------------------------  |
        |  |  frame_plot               |   |   frame_param          |  |
        |  |                           |   |                        |  |
        |  |  ----------------------   |   |   [buttons]            |  |
        |  |  |                    |   |   |   [sliders]            |  |
        |  |  |   canvas_plot      |   |   |   [spin boxes]         |  |
        |  |  |                    |   |   |   [radio buttons]      |  |
        |  |  |                    |   |   |   [progress]           |  |
        |  |  |                    |   |   |                        |  |
        |  |  ----------------------   |   |       ...              |  |
        |  |                           |   |                        |  |
        |  -----------------------------   --------------------------  |
        ----------------------------------------------------------------
        ----------------------------------------------------------------
        |  frame_bottom                                                |
        |                                        [run] ... [quit]      |
        ----------------------------------------------------------------
    """

    PAR = Optional[Union[str, int, float]]
    
    def __init__(self, 
                 identifier: str='Simulate', 
                 path: Optional[str] = None,
                 model: Optional[Callable]=None,
                 labels: List[str]=['x', 'y1', 'y2'],
                 param_list: Optional[List[Tuple[str, PAR, PAR, PAR]]]=None,
                 about_text: Optional[str]=None,
                 help_text: Optional[str]=None,                 
                ) -> None:
        """
        Args 
            identifier
                identifier of simulation
                
            path
                file path to result filee. If None, then tempdir will 
                be assigned 
                
            model
                implementation of user-defined model 
                  model(data: Dict[str, Any], figure: Figure) 
                called in self.simulation()
            
            labels 
                list of axis labels: [x_label, y1_label, y2_label, ...]
                
                Note: length of label list defines number of 
                      subplots, n_subplots = len(labels)-1
        
            param_list:
                List of widget descriptions 
                (
                 (type: str, par_name, par_min, par_max, default),
                 (type, par_name, par_min, par_max, default),
                )
                
                'type' is: 'spin', 'slider', 'entry', or 'check'
                'par_min', 'par_max' and 'default' are optional
                type of 'par_min','par_max','default' is str, int, float
                                
                Note: Tuples with only one member require a comma before 
                      closing parenthesis, 
                      e.g. ('name') is invalid, but ('name',) is OK
        """
        if param_list is None:
            # demo list of widgets
            param_list = (
                ('spin',   'n1', -1, 4),
                ('slider', 'iterations', 0, 500, 50),
                ('slider', 'n2'),
                ('entry',  'f2', None, None, '?'),
                ('slider', 'sl2', -10, 500, 50),
            )
        if about_text is None:
            about_text = 'This is GuiBase1\n\nVersion: 11.19'
        if help_text is None:
            help_text = 'placeholder\nplaceholder\nplaceholder\n'

        self.identifier: str = identifier
        self.path: str = path if path is not None else tempfile.gettempdir() 
        self.root_window: Optional[Any] = None
        self.data: Optional[Dict[str, Any]] = None
 
        self.widgets: Optional[Dict[str, Tuple[Any, Any]]] = OrderedDict()        
        self.i_row: int = 0  # row counter in sub-frame 'frm_param'
        self.labels: List[str] = labels
        self.about_text: str = about_text
        self.help_text: str = about_text
        
        self.param_list = param_list

        self.model: Optional[Callable] = model
        
        print('+++ path:', self.path)

#    def new_file(self) -> Dict[str, Any]:
#        self.data = OrderedDict()
#        return self.data
        
    def update_widget_values(self) -> bool:
        for key, value in self.data.items():
            if key in self.widgets:                
                wdg, var = self.widgets[key]
                if isinstance(wdg, tkinter.Checkbutton):
                    if value:
                        wdg.select()
                    else:
                        wdg.deselect()
                elif isinstance(wdg, tkinter.Entry):
                    wdg.delete(0, tkinter.END)
                    wdg.insert(0, value) 
                elif isinstance(wdg, tkinter.Label):
                    wdg.configure(text=str(value))
                elif isinstance(wdg, tkinter.Scale):
                    wdg.set(value)
                elif isinstance(wdg, tkinter.Spinbox):
                    wdg['value'] = value
                elif wdg is None:
                    print('widget is None, var:', var)
                else:
                    assert 0, str(type(wdg))
        return True

    def open_file(self) -> bool:
        name = filedialog.askopenfilename()
        self.data = json.load(open(name, 'r'))
        ok = self.data is not None
        if ok:
            ok = self.update_widget_values()        
        return ok

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
        sub_txt = tkinter.Text(sub, width=32, height=5) 
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
        if self.data is not None and self.widgets is not None:
            for key, wdg_var in self.widgets.items():
                wdg, var = wdg_var
                if not isinstance(wdg, (tkinter.Label, Progressbar, )):
                    if var is None:
                        self.data[key] = wdg.get()
                    else:
                        self.data[key] = var.get()
                        
        if self.data is None:
            self.data = OrderedDict()
                    
        now = datetime.now()
        self.data['timestamp'] = now.strftime('%Y-%m-%dT%H:%M:%S')      

        file = os.path.join(self.path, '.config.json')
        return json.dump(self.data, open(file, 'w'), indent=4)
    
    def update_and_quit(self) -> None:
        self.update_data()
        self.root_window.destroy()        
        
    def simulate(self) -> float:        
        figure = Figure(figsize=(10, 6))
        
        # canvas can later be accessed via: figure.canvas
        canvas_plot = FigureCanvasTkAgg(figure, master=self.frm_plot)
        canvas_plot.get_tk_widget().grid(row=0, column=0)

        # axes can be accessed via: figure.axes
        axes = figure.subplots(len(self.labels)-1, sharex=True, sharey=True)

        # title above first subplot
#        axes[0].set_title(self.identifier)
        axes[-1].set_xlabel(self.labels[0])
        for i, ax in enumerate(axes):
            ax.set_ylabel(self.labels[i+1])
            ax.grid()
        figure.tight_layout()

        result_label = self.widgets.get('result')
        if result_label is not None:
            result_label[0].configure(text='-  ', anchor='e', borderwidth=2, 
                                      relief='raised')
            
        ### MODEL ###
        if self.model:
            res = self.model(self.data, figure, self.widgets.get('progress'))
        else:
            res = float('inf')

        if 'save figure' in self.widgets and \
                self.widgets['save figure'][1].get():
            f = (self.identifier + '_' + \
                datetime.now().strftime('%Y-%m-%dT%H.%M.%S')).replace(' ', '_')
            f = os.path.join(self.path, f)
            json.dump(self.data, open(f + '.json', 'w'), indent=4)
            figure.savefig(f +'.png')

        if result_label is not None:
            result_label[0].configure(text=str(res), anchor='e', borderwidth=2, 
                                      relief='sunken')
            if res == -1 or res == float('inf'):
                result_label[0].configure(background='red')
        
    def create_menus(self) -> None:
        mainmenu = tkinter.Menu(self.root_window)
        self.root_window.config(menu=mainmenu)
        
        filemenu = tkinter.Menu(mainmenu)
        mainmenu.add_cascade(label='File', menu=filemenu)
#        filemenu.add_command(label='New', command=self.new_file)
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
        frm_top.grid(column=0, row=0, pady=10)
        frm_center = tkinter.Frame(self.root_window)
        frm_center.grid(column=0, row=1, padx=20)
        frm_bottom = tkinter.Frame(self.root_window)
        frm_bottom.grid(column=0, row=2)
        self.frm_param = tkinter.Frame(frm_center)
        self.frm_param.grid(column=1, row=0)
        self.frm_plot = tkinter.Frame(frm_center)
        self.frm_plot.grid(column=0, row=0)

        ## create action buttons 
        pady = 16
        btn_run = tkinter.Button(frm_bottom, text='Run', 
                                 command=self.simulate)
        btn_run.grid(column=0, row=0, padx=10, pady=pady)
            
        btn_quit = tkinter.Button(frm_bottom, text='Quit', 
                                  command=self.update_and_quit)
        btn_quit.grid(column=3, row=0, padx=10, pady=pady)

        # create placeholder reserving space for plotting canvas 
        cnv_dummy = tkinter.Canvas(self.frm_plot, width=800, height=480)
        cnv_dummy.create_rectangle(0+26, 16, 800-30, 480-2*10, fill='white')
        cnv_dummy.grid(row=0, column=0, pady=0)

    def create_parameter_input(self) -> None:
        """
        Creates widgets for parameter input in parameter frame 
        """
        
        pady = 4
        lbl_width = 12
        root = self.root_window 
        self.i_row = 0

        def create_slider(self, key_and_range):
            key = key_and_range[0]
            
            from_ = key_and_range[1] if len(key_and_range) > 1 else 0
            to = key_and_range[2] if len(key_and_range) > 2 else 100
            default = key_and_range[3] if len(key_and_range) > 3 \
                                       else (from_ + to) / 2
            
            wdg = tkinter.Scale(self.frm_param, from_=from_, 
                                to=to, orient=tkinter.HORIZONTAL,
                                resolution = (to - from_) / 100, width = 8,
                                command=self.update_data)
            wdg.set(default)
            wdg.grid(column=0, row=self.i_row, padx=10, pady=pady)
            self.widgets[key] = (wdg, None)

            tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                          anchor='w').grid(column=1, row=self.i_row, 
                                           padx=10, pady=pady)
            self.i_row += 1

        def create_spin_box(self, key_and_range):
            key = key_and_range[0]
            
            from_ = key_and_range[1] if len(key_and_range) > 1 else 0
            to = key_and_range[2] if len(key_and_range) > 2 else 100
            default = key_and_range[3] if len(key_and_range) > 3 else 'abc'
            
            var = tkinter.StringVar(self.frm_param, value=str(default))
            wdg = tkinter.Spinbox(self.frm_param, from_=from_, to=to, width=14, 
                                  textvariable=var, command=self.update_data)
            wdg.grid(column=0, row=self.i_row, padx=10, pady=pady)
            self.widgets[key] = (wdg, var)

            tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                anchor='w').grid(column=1, row=self.i_row, 
                                 padx=10, pady=pady)
            self.i_row += 1

        def create_entry_form(self, key_and_range):
            key = key_and_range[0]
            default = key_and_range[3] if len(key_and_range) > 3 else 'abc'

            var = tkinter.StringVar(self.frm_param, default)
            wdg = tkinter.Entry(self.frm_param, textvariable=var,
                                width=14+2, validate='focusout', 
                                validatecommand=self.update_data)
            wdg.grid(column=0, row=self.i_row, padx=10, pady=pady)
            self.widgets[key] = (wdg, var)

            tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                          anchor='w').grid(column=1, row=self.i_row, padx=10, 
                                           pady=pady)        
            self.i_row += 1

        def create_check_button(self, key_and_range):
            key = key_and_range[0]
            default = key_and_range[3] if len(key_and_range) > 3 else 1

            var = tkinter.IntVar(root)        
            wdg = tkinter.Checkbutton(self.frm_param, variable=var, 
                                      onvalue = 1, offvalue = 0, anchor='e', 
                                      width = 13, command=self.update_data)
            wdg.grid(column=0, row=self.i_row, padx=0, pady=pady)
            if default:
                wdg.select()
            self.widgets[key] = (wdg, var)

            tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                          anchor='w').grid(column=1, row=self.i_row, padx=0, 
                                           pady=pady)        
            self.i_row += 1

        def create_label(self, key_and_range):
            key = key_and_range[0]
            default = key_and_range[3] if len(key_and_range) > 3 else '?'

            wdg = tkinter.Label(self.frm_param, text=default, width=14)
            wdg.grid(column=0, row=self.i_row, padx=10, pady=pady)
            self.widgets[key] = (wdg, None)
            tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                          anchor='w').grid(column=1, row=self.i_row, 
                                           padx=10, pady=pady)        
            self.i_row += 1

        def create_progress_bar(self, key_and_range):
            key = key_and_range[0]
            
            to = key_and_range[2] if len(key_and_range) > 2 else 100
            default = key_and_range[3] if len(key_and_range) > 3 else 'abc'

            sty = tkinter.ttk.Style()
            sty.theme_use('clam')
            sty.configure('gray.Horizontal.TProgressbar')
            wdg = Progressbar(self.frm_param,
                value=default, maximum=to, style='ray.Horizontal.TProgressbar',
                orient='horizontal', length=98, mode='determinate')
            wdg.grid(column=0, row=self.i_row, padx=10, pady=pady)
            self.widgets[key] = (wdg, None)
            tkinter.Label(self.frm_param, text=key, width=lbl_width, 
                anchor='w').grid(column=1, row=self.i_row, 
                                 padx=10, pady=pady)
            self.i_row += 1


        call_creation_of_widget = {
            'spin':     create_spin_box,
            'slider':   create_slider,
            'entry':    create_entry_form,
            'check':    create_check_button,
            'label':    create_label,
            'progress': create_progress_bar,
        }
        
        create_progress_bar(self, ('progress', None, None, 0.)) 

        if self.param_list:
            for par in self.param_list:
                call_creation_of_widget[par[0]](self, par[1:])
        
        create_check_button(self, ('save figure', None, None, False))        
        create_check_button(self, ('silent', None, None, True))        
        create_label(self, ('result', None, None, '?'))        
        self.widgets['result'][0].configure(text='-  ', borderwidth=2, 
                                            relief='raised', anchor='e')

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
