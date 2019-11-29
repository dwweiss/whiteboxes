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

__all__ = ['dialog_yes_no', 'dialog_load_filenames', 'dialog_save_filename',
           'dialog_directory', 'dialog_info']

import os
from typing import List, Optional
try:
    import tkinter
    from tkinter import filedialog, messagebox 
except ImportError:
    import sys
    print("\n!!! Wrong Python interpreter (version: '" +
          str(sys.version_info.major) + '.' + str(sys.version_info.major) +
          '.' + str(sys.version_info.micro) + "') or 'tkinter' not imported")


def dialog_yes_no(title: str = '', icon: str = '') -> str:
    """
    Asks for Yes/No employing tkinter interface

    Args:
        title:
            box title

        icon:
            icon to be displayed

    Returns:
        answer: 
            'Yes' or 'No'
    """
    tkinter.Tk().withdraw()
    result = messagebox.askquestion(title=title, icon=icon)
    return result


def dialog_load_filenames(default_ext: str = 'data', 
                          initial_dir: Optional[str] = None,
                          min_files: int = 1) -> List[str]:
    """
    Asks for one or more file names to be loaded, employing tkinter interface

    Args
        default_ext:
            default file extension

        initial_dir:
            directory where selection starts

        min_files:
            minimum number of file names, dialog will be repeated if number
            is not reached or file names are not unique

    Returns
        list of full paths to selected file(s)
    """
    if not initial_dir:
        initial_dir = os.getcwd()

    tkinter.Tk().withdraw()
    result = []
    first = True
    while len(result) < min_files:
        filenames = filedialog.askopenfilenames(initialdir=initial_dir,
            title='Select files', multiple=True,
            defaultextension=default_ext)
        if first:
            first = False
        if not first:
            initial_dir = os.path.dirname(filenames[-1])
        for name in filenames:
            if name not in result:
                result += [name, ]

    return result


def dialog_save_filename(default_ext: str = 'data', 
                         initial_dir: Optional[str] = None,
                         confirm_overwrite: bool = True) -> List[str]:
    """
    Asks for file name to be saved, employing tkinter interface

    Args
        default_ext:
            default file extension

        initial_dir:
            directory where selection starts

        confirm_overwrite:
            if False, file will be overwritten without warning

    Returns
        full paths to selected file
    """
    if not initial_dir:
        initial_dir = os.getcwd()

    tkinter.Tk().withdraw()
    result = filedialog.asksaveasfile(initialdir=initial_dir,
        title='Select files', defaultextension=default_ext,
        confirmoverwrite=confirm_overwrite)

    return result.name


def dialog_directory(initial_dir: Optional[str] = None) -> str:
    """
    Asks for directory, employing tkinter interface

    Args
        initial_dir:
            directory where selection starts

    Returns
        path to selected directory
    """
    if not initial_dir:
        initial_dir = os.getcwd()

    tkinter.Tk().withdraw()
    directory = filedialog.askdirectory(initialdir=initial_dir,
        title='Select directory')

    return directory


def dialog_info(title: str = '', message: str = '') -> None:
    """
    Displays information

    Args:
        title:
            box title

        message:
            text to be displayed
    """
    tkinter.Tk().withdraw()
    messagebox.showinfo(title=title)
