from __future__ import print_function

from bokeh.io import curdoc

# import all custom classes
#from bokeh.plotting import FunctionPlotter
from function_plotter import FunctionPlotter
#import function_plotter as fp
#print(__file__)
#import imp
#test = imp.load_source("function_plotter", "/home/tobias/git/bokeh_start_app/bokeh_start_app/bokeh_apps/function_plotter/function_plotter.py")
#print(test)

fp = FunctionPlotter(name='bk-function-plotter')

args = curdoc().session_context.request.arguments
print(args)
if 'f' in args:
    fp.change_function(args['f'][0])

curdoc().add_root(fp)
curdoc().title = "Function plotter"
#curdoc().session_context['fp'] = fp
# set a new single key/value
#curdoc().template_variables["user_id"] = "test"
