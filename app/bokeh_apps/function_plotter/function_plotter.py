from __future__ import print_function

import numpy as np

from bokeh.plotting import Figure
from bokeh.models import (ColumnDataSource, Line)
from bokeh.core.properties import Enum, Int, Instance, String, Float
import re

# copy this function manually to bokeh/plotting
class FunctionPlotter(Figure):
    __view_model__ = "Plot"
    #__subtype__ = "FunctionPlotter"
    __subtype__ = "FunctionPlotter" # needs to be in bokeh.plotting


    source = Instance(ColumnDataSource)
    function = String(default="")
    start = Float(default=10)
    end = Float(default=-10)
    points = Int(default=1000)

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.source = ColumnDataSource(data={'x':[],'y':[]})
        self.update()
        #self.__class__ = Figure
        #self.line(x='x',y='y',source=self.source)


    def change_function(self,function):
        self.function=function
        self.update()

    def change_limits(self,start,end):
        self.start = float(start)
        self.end = float(end)
        self.update()

    def update(self):
        if self.function != "":
            print ("Update to function '{}' from {} to {}.".format(self.function,self.start,self.end))
            func = self.__string2func(self.function)
            x = np.linspace(self.start, self.end, self.points)
            self.source = ColumnDataSource(data={'x':x,'y':func(x)})
            self.line(x='x',y='y',source=self.source)
            #self.source.data={'x':x,'y':func(x)}
        else:
            print("No update, function empty!")

    def plot(self):
        return super(self.__class__, self)


    def __replacements(self):
        return {
            'sin' : 'np.sin',
            'cos' : 'np.cos',
            'tan' : 'np.tan',
            'exp': 'np.exp',
            'sqrt': 'np.sqrt',
            '^': '**',
        }

    def __allowed_words(self):
        return [
            'x',
            'sin',
            'tan',
            'cos',
            'sqrt',
            'exp',
        ]

    def __string2func(self,string):
        ''' evaluates the string and returns a function of x '''
        # find all words and check if all are allowed:
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in self.__allowed_words():
                raise ValueError(
                    '"{}" is forbidden to use in math expression'.format(word)
                )

        for old, new in self.__replacements().items():
            string = string.replace(old, new)

        def func(x):
            try:
                return eval(string)
            except:
                print("Evaluation of '{}' did not work.".format(string))
                return eval("x")

        return func
