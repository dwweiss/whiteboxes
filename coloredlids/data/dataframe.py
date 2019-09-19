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
      2019-03-21 DWW
"""

__all__ = ['split_frame', 'select_frame', 'xy_to_frame', 'frame_to_xy',
           'excel_to_xy', 'xy_to_excel', 'ansys_csv_to_frame']


from typing import Optional, Sequence, Tuple, Union
from collections import OrderedDict
from pandas import read_csv, read_excel, DataFrame, ExcelWriter
import numpy as np
from tempfile import gettempdir


def split_frame(df: DataFrame,
                split_col: Optional[str]=None, 
                sort_col: Optional[str]=None, 
                min_sub_frame_size: int=1) -> Sequence[OrderedDict]:
    """
    Splits data frame 'df' into an ordered dictionary of sub-data 
    frames. In every sub-DataFrame the values in the column with the 
    identifier 'split_col' are equal  

    Sorts optionally the rows of every sub-DataFrame according to 
        values in 'sort_col' column (ascending)

    Args:
        df:
            single data frame

        split_col:
            identifier of column used for splitting of 'df'

        sort_col:
            identifier of column used for sorting every sub-frame,
            no sorting if 'sort_col' is empty

        min_sub_frame_size:
            minimum size of sub-data frame. Smaller sizes are excluded 
            from the returned dictionary of sub-DataFrames

    Returns:
        dictionary of data frames with equal 'split_col' values 

    Note:
        keys of the OrderedDict are of same type as values in 
        'split_col' column of 'df'
    """
    split_value_variations = df[split_col].unique().tolist()
    subFrames = OrderedDict()
    for val in split_value_variations:
        sub = df.loc[df[split_col] == val]
        if len(sub.index) >= min_sub_frame_size:
            if sort_col:
                sub.sort_values(by=[sort_col], ascending=[True], inplace=True)
            sub.index = range(len(sub.index))
            subFrames[val] = sub
    return OrderedDict(sorted(subFrames.items()))


def select_frame(df: DataFrame, 
                 par_col: Union[str, Sequence[str]], 
                 op_sel: Union[str, Sequence[str]], 
                 val_sel: Union[str, float, int, 
                                Sequence[Union[str, float, int]]],
                 sort_col: Optional[str]=None) -> DataFrame:
    """
    Extract single sub-frame of given pandas.DataFrame; selection can be
    based on multiple conditions employing the
    operators  ['==', '!=', '<>', '>', '>=', '<', '<=']

    Args:
        df:
            single data frame

        par_col:
            identifier of column used for selection

        op_sel:
            operator for comparing elements of column 'df[par_col]' with 
            'val_sel'

        val_sel:
            selection value in column used for extraction

        sort_col:
            column key used for sorting; no sorting if 'sort_col' is None

    Returns:
        data frame with rows fulfilling the condition 
            'df(i, par_sel)  <op_sel>  val_sel'

    Note:
        Length of 'par_sel' must not greater than length of 'val_sel'.
        If 'par_sel' and 'val_sel' are lists or tuples, then the size of 
        'op_sel' will be corrected if too short
    """
    if par_col is None:
        return df
    if isinstance(par_col, str):
        par_col = [par_col]
    if isinstance(par_col, tuple):
        par_col = list(par_col)
    if not op_sel:
        op_sel = '=='
    if isinstance(op_sel, str):
        op_sel = [op_sel]
    if isinstance(op_sel, tuple):
        op_sel = list(op_sel)
    op_sel = [x if x else '==' for x in op_sel]
    if isinstance(val_sel, (int, float, str, bool)):
        val_sel = [val_sel]
    if isinstance(val_sel, tuple):
        val_sel = list(val_sel)

    for i in range(len(op_sel), len(par_col)):
        op_sel.append(op_sel[0])
    assert len(par_col) == len(val_sel), 'len(par) != len(val)='

    for x in op_sel:
        assert any([x == o for o in
                   ['=', '==', '!=', '>', '>=', '<', '<=']]), \
               'invalid operator'
    assert len(par_col) == len(val_sel), 'incompatible parameters'

    subFrames = df

    for o, p, v in zip(op_sel, par_col, val_sel):
        if o == '==' or o == '=':
            subFrames = subFrames.loc[subFrames[p] == v]
        elif o == '!=':
            subFrames = subFrames.loc[subFrames[p] != v]
        elif o == '>':
            subFrames = subFrames.loc[subFrames[p] > v]
        elif o == '>=':
            subFrames = subFrames.loc[subFrames[p] >= v]
        elif o == '<':
            subFrames = subFrames.loc[subFrames[p] < v]
        elif o == '<=':
            subFrames = subFrames.loc[subFrames[p] <= v]
        else:
            assert 0, 'unknown operator'

    if sort_col:
        subFrames = subFrames.sort_values(by=sort_col)
    return subFrames


def xy_to_frame(X : np.ndarray, 
                Y : np.ndarray, 
                x_keys: Optional[Sequence[str]]=None, 
                y_keys: Optional[Sequence[str]]=None) -> DataFrame:
    """
    Converts two 2D arrays to pandas.DataFrame

    Args:
        X:
            input 2D array, first index is data point index

        Y:
            output 2D array,first index is data point index

        x_keys:
            column indentifiers of inputs

        y_keys:
            column indentifiers of outputs

    Returns:
        data frame created from X and Y arrays
    """
    assert x_keys is None or X is None or len(x_keys) == X.shape[1]
    assert y_keys is None or Y is None or len(y_keys) == Y.shape[1]
    if X and Y:
        assert X.shape[0] == Y.shape[0]

    if x_keys is None:
        if X is not None:
            x_keys = ['x' + str(i) for i in range(X.shape[1])]
        else:
            x_keys = []
    if y_keys is None:
        if Y is not None:
            y_keys = ['y' + str(i) for i in range(Y.shape[1])]
        else:
            y_keys = []
        
    dic = OrderedDict()
    for j in range(len(x_keys)):
        dic[x_keys[j]] = X[:, j]
    for j in range(len(y_keys)):
        dic[y_keys[j]] = Y[:, j]
    return DataFrame(dic)


def frame_to_xy(df: DataFrame, 
                x_keys: Optional[Sequence[str]]=None, 
                y_keys: Optional[Sequence[str]]=None) \
        -> Tuple[np.ndarray, np.ndarray]:
    """
    Converts pandas.DataFrame to couple of 2D arrays
    
    See also: grayboxes.boxmodel.frame2arr()

    Args:
        df:
            data frame

        x_keys:
            list of input keys

        y_keys:
            list of output keys

    Returns:
        X:
            2D array of independent variables

        Y:
            2D array of dependent variables
    """
    x_keys = list(x_keys) if x_keys is not None else []
    y_keys = list(y_keys) if y_keys is not None else []
    assert all(k in df for k in x_keys), \
        'unknown x-keys: ' + str(x_keys) + ', valid keys: ' + df.columns
    assert all(k in df for k in y_keys), \
        'unknown y-keys: ' + str(y_keys) + ', valid keys: ' + df.columns

    return np.asfarray(df.loc[:, x_keys]), np.asfarray(df.loc[:, y_keys])


def excel_to_xy(x_keys: Optional[Sequence[str]]=None, 
                y_keys: Optional[Sequence[str]]=None, 
                file: str=gettempdir(),
                sheet_name: str='data', 
                startcol: int=0, 
                startrow: int=0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Reads data frame from excel file and converts it to two 2D arrays

    Args:
        x_keys:
            list of input keys

        y_keys:
            list of output keys

        file:
            full path to Excel file

        sheet_name:
            name of Excel sheet

        startcol:
            start column in sheet

        startrow:
            start row in sheet


    Returns:
        X:
            independent variables in 2D array

        Y:
            dependent variables in 2D array
    """
    df = read_excel(open(file, 'rb'),
                    sheetname=sheet_name, startcol=startcol, startrow=startrow)
    return frame_to_xy(df, x_keys, y_keys)


def xy_to_excel(X: np.ndarray, 
                Y: Optional[np.ndarray]=None, 
                x_keys: Optional[Sequence[str]]=None, 
                y_keys: Optional[Sequence[str]]=None,
                file: str=gettempdir(),
                sheet_name: str='data', 
                startcol: int=0, 
                startrow: int=0) -> bool:
    """
    Converts two 2D arrays to DataFrame and write it to excel file

    Args:
        X:
            2D array of input 

        Y:
            2D array of output 

        x_keys:
            list of input keys

        y_keys:
            list of output keys

        file:
            full path to Excel file

        sheet_name:
            name of Excel sheet

        startcol:
            start column in sheet

        startrow:
            start row in sheet

    Returns:
        False if file cannot be opended for writing
    """
    df = xy_to_frame(X, Y, x_keys, y_keys)
    writer = ExcelWriter(file)
    if not writer:
        return False

    df.to_excel(writer, sheet_name=sheet_name, startcol=startcol,
                startrow=startrow)
    writer.save()
    return True


def ansys_csv_to_frame(file: str, 
                       sort_col: Optional[str]=None, 
                       clean: bool=True, 
                       silent: bool=False) -> DataFrame:
    """
    Reads csv-file of results from Ansys, removes 'Pxx - '-prefix from 
    column names, and removes columns whose keys contain postfix '.FD'

    Args:
        file:
            full path to file

        sort_col:
            identifier of column for sorting, no sorting if not 'sort_col'

        clean:
            if True, remove 'NaN' and duplicated rows

        silent:
            if True, suppress output to console

    Returns:
        data frame of floats

    Example:
        #
        # 01/01/2017 09:30:18
        # The parameters defined in the project are:
        # ,P2 - r [mm],P9 - w [mm],P11 - h [mm] ...
        #
        # The following header line defines the name of the columns by ref ...
        Name,P2,P9,P11, ...
        DP 0,112.5,60,40, ...
        DP 1,112.5,60,40, ...
        ...
    """
    i_line_human_readable_keys = 3  # ind.of line with human readab.keys
    n_header_lines = 6            # number of header lines to be skipped

    # read list of human readable keys from line 3 (zero-based)
    keys = None
    try:
        with open(file) as fp:
            for i, line in enumerate(fp):
                if i == i_line_human_readable_keys:
                    keys = line[:-1].split(',')
                    break
        fp.close()
    except IOError:
        if not silent:
            print("\n???\n??? file: '" + file + "' does not exist\n???\n")
        raise Exception('')

    keys = keys[1:]  # skipping 'Name' in first non-commented line
    human_readable_keys = ['idDesignPoint']
    for key in keys:
        key = key.split(' - ')[1]  # second part after '-'
        # remove multiple space
        human_readable_keys.append(' '.join(key.split()))  

    # read data frame with non-human readable column keys
    data = read_csv(file, comment='#', skiprows=n_header_lines)

    # replace non-human readable column keys with human redadable ones
    data.columns = human_readable_keys

    # remove columns with design point index and keys containing '.FD'
    data.drop('idDesignPoint', axis=1, inplace=True)
    for col in data.columns:
        if '.FD' in col:
            data.drop(col, axis=1, inplace=True)

    # sort data frame
    if sort_col:
        if not silent:
            print("    Sort: '" + str(sort_col) + "'")
        data.sort_values(by=[sort_col], ascending=[True], inplace=True)

    l = list(data.columns)
    d = set([x for x in l if l.count(x) > 1])
    assert len(d) == 0, '\n\n??? Duplicated columns:\n\n' + str(d)

    # remove NaN and duplicates
    if clean:
        if not silent:
            print('    Clean data')
        data = data.dropna(how='any')
        data.drop_duplicates(keep='last', inplace=True)
        data = data.astype('float')

    return data
