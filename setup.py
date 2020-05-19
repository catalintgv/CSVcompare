#python setup.py bdist_msi  pentru creare msi
#python setup.py build  pentru creare exe

from cx_Freeze import setup, Executable
import os
import sys

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

exe = [Executable("mainCSV.py", base=base, icon='csv.ico')]

os.environ['TCL_LIBRARY'] = r'C:\\Users\\dm\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\dm\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6'

options = {
'build_exe': {
    'include_files': ['ico.png','cross-script.png','untitled.ui'],
    'packages': ['pyqt5']
}
}

setup(name="CSV file comparer", version="1.0", description='Compare two csv files',
  options=options, executables=exe)