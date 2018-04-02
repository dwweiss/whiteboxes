"""
  Copyright (c) 2016-17 by Dietmar W Weiss

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
      2017-11-16 DWW
"""


from collections import OrderedDict
from pandas import read_csv
import numpy as np


def split(df, split, sort=None, minSubFrameSize=1):
    """
    Splits DataFrame into OrderedDictionary of sub-DataFrames. The value of the
        'split' column is equal in every sub-DataFrame.
    Sorts optionally the rows of every sub-DataFrame according to values in
        'sort' column (ascending).

    Args:
        df (pandas.DataFrame):
            single data frame

        split (string):
            identifier of column used for splitting data frame

        sort (string):
            identifier of column used for sorting every sub-frame,
            no sorting if 'sort' is empty

        minSubFrameSize (int):
            minimum size of sub-DataFrame; smaller sizes are excluded

    Returns:
        collections.OrderedDictionary (data values in 'split' column are used
        as keys)

    Note:
        The keys of the OrderedDictionary are of the same type as the values in
        the 'split' column of 'data'
    """
    splitValueVariations = df[split].unique().tolist()
    subFrames = OrderedDict()
    for val in splitValueVariations:
        sub = df.loc[df[split] == val]
        if len(sub.index) >= minSubFrameSize:
            if sort:
                sub.sort_values(by=[sort], ascending=[True], inplace=True)
            sub.index = range(len(sub.index))
            subFrames[val] = sub
    return OrderedDict(sorted(subFrames.items()))


def select(df, par, op, val, sort=None):
    """
    Extract single sub-frame of given pandas.DataFrame; selection can be
    based on multiple conditions employing the
    operators  ['==', '!=', '<>', '>', '>=', '<', '<=']

    Args:
        df (pandas.DataFrame):
            single data frame

        par (string, or list/tuple of string):
            identifier of column used for filtering

        op (string, or list/tuple of string):
            operator for comparing elements of column 'df[par]' with 'val'

        val (string, float, int, or list/tuple of string, float, int):
            selection value in column used for extraction

        sort (string):
            key of column used for sorting; no sorting if 'sort' is None

    Returns:
        pandas.DataFrame containing rows fulfilling condition:
        (df(i, par) 'op' val)

    Note:
        Length of 'par' must not be greater than length of 'val' if both are
        list/tuple; 'op' will be corrected if too short
    """
    if par is None:
        return df
    if isinstance(par, str):
        par = [par]
    if isinstance(par, tuple):
        par = list(par)
    if not op:
        op = '=='
    if isinstance(op, str):
        op = [op]
    if isinstance(op, tuple):
        op = list(op)
    op = [x if x else '==' for x in op]
    if isinstance(val, (int, float, str, bool)):
        val = [val]
    if isinstance(val, tuple):
        val = list(val)

    for i in range(len(op), len(par)):
        op.append(op[0])
    assert len(par) == len(val), 'len(par) != len(val)='

    for x in op:
        assert any([x == o for o in
                   ['=', '==', '!=', '>', '>=', '<', '<=']]), \
               'invalid operator'
    assert len(par) == len(val), 'incompatible parameters'

    subFrames = df

    for o, p, v in zip(op, par, val):
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

    if sort:
        subFrames = subFrames.sort_values(by=sort)
    return subFrames


def xy2frame(X, Y, xKeys=None, yKeys=None):
    """
    Converts two 2D arrays to pandas.DataFrame

    Args:
        X (2D array of float):
            input array, first index is data point index

        Y (2D array of float):
            output array,first index is data point index

        xKeys (list of string):
            column indentifiers of inputs

        yKeys (list of string):
            column indentifiers of outputs

    Returns:
        pandas.DataFrame created from X and Y arrays
    """
    assert xKeys is None or X is None or len(xKeys) == X.shape[1]
    assert yKeys is None or Y is None or len(yKeys) == Y.shape[1]
    assert X.shape[0] == Y.shape[0]

    if xKeys is None:
        if X is not None:
            xKeys = ['x' + str(i) for i in range(X.shape[1])]
        else:
            xKeys = []
    if yKeys is None:
        if Y is not None:
            yKeys = ['y' + str(i) for i in range(Y.shape[1])]
        else:
            yKeys = []
    dic = OrderedDict()
    for j in range(len(xKeys)):
        dic[xKeys[j]] = X[:, j]
    for j in range(len(yKeys)):
        dic[yKeys[j]] = Y[:, j]
    return DataFrame(dic)


def frame2xy(df, xKeys, yKeys):
    """
    Converts pandas.DataFrame to two 2D arrays

    Args:
        df (pandas.DataFrame):
            data frame

        xKeys (list of string):
            list of input keys

        yKeys (list of string):
            list of output keys

    Returns:
        X (2D numpy array of float):
            independent variables

        Y (2D numpy array of float):
            dependent variables
    """
    xKeys = list(xKeys) if xKeys is not None else []
    yKeys = list(yKeys) if yKeys is not None else []
    assert all(k in df for k in xKeys), \
        'unknown x-keys: ' + str(xKeys) + ', valid keys: ' + df.columns
    assert all(k in df for k in yKeys), \
        'unknown y-keys: ' + str(yKeys) + ', valid keys: ' + df.columns
    return np.asfarray(df.loc[:, xKeys]), np.asfarray(df.loc[:, yKeys])


def excel2xy(xKeys=None, yKeys=None, file='c:/temp/data.xlsx',
             sheetname='data', startcol=0, startrow=0):
    """
    Reads DataFrame from excel file and convert it to two 2D arrays

    Args:
        file (string):
            full path to Excel file

        sheetname (string):
            name of Excel sheet

        startcol (int):
            start column in sheet

        startrow (int):
            start row in sheet

        xKeys (list of string):
            list of input keys

        yKeys (list of string):
            list of output keys

    Returns:
        X (2D numpy array of float):
            independent variables

        Y (2D numpy array of float):
            dependent variables
    """
    df = read_excel(open(file, 'rb'),
                    sheetname=sheetname, startcol=startcol, startrow=startrow)
    return frame2xy(df, xKeys, yKeys)


def xy2excel(X, Y=None, xKeys=None, yKeys=None, file='c:/temp/data.xlsx',
             sheetname='data', startcol=0, startrow=0):
    """
    Converts two 2D arrays to DataFrame and write it to excel file

    Args:
        xKeys (list of string):
            list of input keys

        yKeys (list of string):
            list of output keys

        file (string):
            full path to Excel file

        sheetname (string):
            name of Excel sheet

        startcol (int):
            start column in sheet

        startrow (int):
            start row in sheet

    Returns:
        False if file cannot be opended for writing
    """
    df = xy2frame(X, Y, xKeys, yKeys)
    writer = ExcelWriter(file)
    if not writer:
        return False
    df.to_excel(writer, sheet_name=sheetname, startcol=startcol,
                startrow=startrow)
    writer.save()
    return True


def loadAnsysCsv(file, sort='', clean=True, silent=False):
    """
    Reads csv-file of results from Ansys, removes 'Pxx - '-prefix from column
    names, and removes columns whose keys contain postfix '.FD'

    Args:
        file (string):
            full path to file

        sort (string):
            identifier of column for sorting, no sorting if 'sort' is empty

        clean (bool):
            if True, remove 'NaN' and duplicated rows

        silent (bool):
            if True, suppress output to console

    Returns:
        pandas.DataFrame

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
    iLineHumanReadableKeys = 3  # index of line with human redable keys
    nHeaderLines = 6            # number of header lines to be skipped

    # read list of human readable keys from line 3 (zero-based)
    keys = None
    try:
        with open(file) as fp:
            for i, line in enumerate(fp):
                if i == iLineHumanReadableKeys:
                    keys = line[:-1].split(',')
                    break
        fp.close()
    except IOError:
        if not silent:
            print("\n???\n??? file: '" + file + "' does not exist\n???\n")
        raise Exception('')
    keys = keys[1:]  # skipping 'Name' in first non-commented line
    humanReadableKeys = ['idDesignPoint']
    for key in keys:
        key = key.split(' - ')[1]  # second part after '-'
        humanReadableKeys.append(' '.join(key.split()))  # del multiple space

    # read data frame with non-human readable column keys
    data = read_csv(file, comment='#', skiprows=nHeaderLines)

    # replace non-human readable column keys with human redadable ones
    data.columns = humanReadableKeys

    # remove columns with design point index and keys containing '.FD'
    data.drop('idDesignPoint', axis=1, inplace=True)
    for col in data.columns:
        if '.FD' in col:
            data.drop(col, axis=1, inplace=True)

    # sort data frame
    if sort:
        if not silent:
            print("    Sort: '" + str(sort) + "'")
        data.sort_values(by=[sort], ascending=[True], inplace=True)

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


# Examples ####################################################################

if __name__ == '__main__':
    from pandas import DataFrame

    df = DataFrame({'x': [10, 32, 20, 40, 10],
                    'y': [31, 41, 41, 31, 10],
                    'z': [32, 61, 44, 33, 7]})
    print('*** \ndf:\n', df)

    if 1:
        print('\n*** get value from pandas.DataFrame(rowIndex, columnKey)')

        # reset_index() ensures that 'index' equals 'range(len(df.index))'
        df.reset_index(inplace=True)
        print("df.get_value(2, 'y'):", df.get_value(2, 'y'))

    if 1:
        print('\n*** Example: select()')

        sub = select(df=df, par=['x', 'y', 'z'],
                     op=['<', '>=', '>='], val=[40, 41, 33], sort='x')
        print(sub)
        sub = select(df, 'x', '!=', 32)
        print('sub:\n', sub)
        sub = select(df, ('x', 'z'), '==', (10, 61))
        print('sub:\n', sub)
        sub = select(df, ['x', 'y'], ['!=', '>='], [40, 41])
        print('sub:\n', sub)
        sub = select(df, par='x', op='==', val=32)
        print('sub:\n', sub)

    if 1:
        print('\n*** Example: split()')

        print('*** \ndf:\n', df)
        orderedDict = split(df, split='y', sort='x')
        print('orderedDict:\n', orderedDict)

    if 1:
        import matplotlib.pyplot as plt
        print('\n*** Example: df.plot()')

        df.plot()
        plt.show()
        df.plot(x='x', y='z')
        df['y'].plot()
        plt.plot(df['x'], df['y'], label='y(x)')
        plt.legend()
        plt.show()

    if 1:
        from pandas import ExcelWriter, read_excel
        print('*** Example: ExcelWriter(), read_excel() and to_csv()')

        file = 'c:/temp/PythonExport.xlsx'
        writer = ExcelWriter(file)
        df.to_excel(writer, sheet_name='data', startcol=4, startrow=3)
        writer.save()
        df.to_csv(file + '.csv', sep=',')

        df2 = read_excel(open(file, 'rb'), sheetname='data',
                         # startcol=4, startrow=3
                         )
        print('\ndf2:\n', df2)

        if 0:
            print('*** Example: Show file in Excel')
            import os
            os.system('start ' + file)

        if 1:
            print('*** Example: Show file in Excel')
            import subprocess
            p = subprocess.Popen(['start', file], shell=True)
            p.wait()

    if 1:
        from pandas import Panel
        print('\n*** Example: Panel()')

        p = Panel({'a': df, 'b': df})
        p['b']['x'][1] = 11111
        p['b']['x'].tun = False
        p['b']['x'].com = True
        del df
        print('-' * 40)
        for label, frame in p.iteritems():
            print('label:', label, 'frame:\n', frame)
            for key, col in frame.items():
                print('key:', key, 'col:', col.tolist())
        print('-' * 40)
        print('p.iloc1:', p.iloc[1])
        print('p,a:', p['a'])
        print('p,b:', p['b'])
        print('p,b,x:', p.loc['b']['x'])
        print('p,b,x,1:', p.loc['b']['x'][1])
        print("p['b']['x'].tun:", p['b']['x'].tun)
        print("p['b']['x'].com:", p['b']['x'].com)
