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
      2019-09-19 DWW
"""

import __init__
__init__.init_path()

import unittest
import os
import subprocess
from tempfile import gettempdir
from pandas import DataFrame, ExcelWriter, read_excel
import matplotlib.pyplot as plt

from coloredlids.data.dataframe import select_frame, split_frame


class TestUM(unittest.TestCase):
    def setUp(self):
        print('///', os.path.basename(__file__))

        self.df = DataFrame({'x': [10, 32, 20, 40, 10],
                             'y': [31, 41, 41, 31, 10],
                             'z': [32, 61, 44, 33, 7]})
        print('***\ndf:\n', self.df)

    def tearDown(self):
        pass

    def test1(self):
        print('\n*** get value from pandas.DataFrame(rowIndex, columnKey)')

        # reset_index() ensures that 'index' equals 'range(len(df.index))'
        df = self.df
        df.reset_index(inplace=True)
        print("df.get_value(2, 'y'):", df.get_value(2, 'y'))

        self.assertTrue(True)

    def test2(self):
        print('\n*** Example: select()')

        df = self.df
        sub = select_frame(df=df, par_col=['x', 'y', 'z'],
                           op_sel=['<', '>=', '>='],
                           val_sel=[40, 41, 33], sort_col='x')
        print(sub)
        sub = select_frame(df, 'x', '!=', 32)
        print('sub:\n', sub)
        sub = select_frame(df, ('x', 'z'), '==', (10, 61))
        print('sub:\n', sub)
        sub = select_frame(df, ['x', 'y'], ['!=', '>='], [40, 41])
        print('sub:\n', sub)
        sub = select_frame(df, par_col='x', op_sel='==', val_sel=32)
        print('sub:\n', sub)

        self.assertTrue(True)

    def test3(self):
        print('\n*** Example: split()')

        df = self.df
        print('*** \ndf:\n', df)
        ordered_dict = split_frame(df, split_col='y', sort_col='x')
        print('orderedDict:\n', ordered_dict)

        self.assertTrue(True)

    def test4(self):
        print('\n*** Example: df.plot()')

        df = self.df
        df.plot()
        plt.show()
        df.plot(x='x', y='z')
        df['y'].plot()
        plt.plot(df['x'], df['y'], label='y(x)')
        plt.legend()
        plt.show()

        self.assertTrue(True)

    def test5(self):
        print('*** Example: ExcelWriter(), read_excel() and to_csv()')

        df = self.df
        file = os.path.join(gettempdir(), 'PythonExport.xlsx')
        writer = ExcelWriter(file)
        df.to_excel(writer, sheet_name='data', startcol=4, startrow=3)
        writer.save()
        df.to_csv(file + '.csv', sep=',')

        df2 = read_excel(open(file, 'rb'), sheetname='data',
                         # startcol=4, startrow=3
                         )
        print('\ndf2:\n', df2)

        self.assertTrue(True)

    def test6(self):
        print('*** Example: Show file in Excel, system()')

        file = os.path.join(gettempdir(), 'PythonExport.xlsx')
        os.system('start ' + file)

        self.assertTrue(True)

    def test7(self):
        print('*** Example: Show file in Excel, subprocess()')

        file = os.path.join(gettempdir(), 'PythonExport.xlsx')
        p = subprocess.Popen(['start', file], shell=True)
        p.wait()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
