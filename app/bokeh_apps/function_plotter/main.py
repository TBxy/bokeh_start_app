from __future__ import print_function

from bokeh.io import curdoc

# import all custom classes
from bokeh.plotting import FunctionPlotter
#import function_plotter as fp
#print(__file__)
#import imp
#test = imp.load_source("function_plotter", "/home/tobias/git/bokeh_start_app/bokeh_start_app/bokeh_apps/function_plotter/function_plotter.py")
#print(test)

p = FunctionPlotter(name='bk-function-plotter')
curdoc().add_root(p)
curdoc().title = "Function plotter"
