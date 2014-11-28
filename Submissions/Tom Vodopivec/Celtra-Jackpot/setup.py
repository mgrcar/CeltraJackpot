# How to use in PyScripter: Run --> Command line parameters --> "py2exe" --> Run
import py2exe
import inspect, os
from distutils.core import setup

setup(console=['Jackpot.py'])
#os.startfile(".\\dist\\Jackpot.exe")
