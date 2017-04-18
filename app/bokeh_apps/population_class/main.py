""" To view this example, first start a Bokeh server:

    bokeh serve --allow-websocket-origin=localhost:8000

And then load the example into the Bokeh server by
running the script:

    python widget.py

in this directory. Finally, start a simple web server
by running:

    python -m SimpleHTTPServer  (python 2)

or

    python -m http.server  (python 3)

in this directory. Navigate to

    http://localhost:8000/widget.html

"""
from __future__ import print_function

from numpy import pi

from bokeh.client import push_session
from bokeh.document import Document
from bokeh.io import curdoc
from bokeh.embed import autoload_server
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.models import (Plot, DataRange1d, LinearAxis, CategoricalAxis,
                          Legend, ColumnDataSource, Grid, Line, Model,
                          SingleIntervalTicker, Quad, Select, FactorRange, LayoutDOM, Row, Box)
from bokeh.sampledata.population import load_population

from bokeh.core.properties import Bool, Enum, Int, Instance, List, Seq, String

#document = Document()

#session = push_session(document)


#class PyramidPlot(Plot):
#
#    def __init__(self,source, **kwargs):
#        xdr = DataRange1d()
#        ydr = DataRange1d()
#        kwargs['title']=None
#        kwargs['x_range']=xdr
#        kwargs['y_range']=ydr
#        kwargs['plot_width']=700
#        kwargs['plot_height']=400
#        super(PyramidPlot, self).__init__(**kwargs)
#
#        xaxis = LinearAxis()
#        self.add_layout(xaxis, 'below')
#        yaxis = LinearAxis(ticker=SingleIntervalTicker(interval=5))
#        self.add_layout(yaxis, 'left')
#
#        self.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
#        self.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
#
#        male_quad = Quad(left="male", right=0, bottom="groups", top="shifted", fill_color="#3B8686")
#        male_quad_glyph = self.add_glyph(source, male_quad)
#
#        female_quad = Quad(left=0, right="female", bottom="groups", top="shifted", fill_color="#CFF09E")
#        female_quad_glyph = self.add_glyph(source, female_quad)
#
#        self.add_layout(Legend(legends=[("Male", [male_quad_glyph]), ("Female", [female_quad_glyph])]))
#
#        #return plot





class Population(Row):

    #print ( "IMPLEMENTATION: {}".format(__implementation__))
    #__implementation__ = super(Population, self).__implementation__
    __view_model__ = "Row"
    __subtype__ = "Population"
    #print ( "IMPLEMENTATION: {}".format(__implementation__))

    #children = List(Instance(LayoutDOM), help="""
    #The list of children, which can be other components including plots, rows, columns, and widgets.
    #""")


    def __init__(self,*args, **kwargs):
        self._df = load_population()
        self._revision = 2012

        self._year = 2010
        self._location = "World"

        self._years = [str(x) for x in sorted(self._df.Year.unique())]
        self._locations = sorted(self._df.Location.unique())

        self._source_pyramid = ColumnDataSource(data=dict())
        self._source_known = ColumnDataSource(data=dict(x=[], y=[]))
        self._source_predicted = ColumnDataSource(data=dict(x=[], y=[]))
        #self._pyramid_plot = PyramidPlot(source=self._source_pyramid,name='bk-pyramid')
        self.update_data()

        kwargs["children"] = [self.layout()]
        #kwargs["children"] = list()
        #kwargs["children"] = list(self.layout)
        self.children.append(self.layout)
        super(Population, self).__init__()
        #self.layout()
        #super(**kwargs)



    def pyramid_plot_old(self):
        xdr = DataRange1d()
        ydr = DataRange1d()

        plot = Plot(title=None, x_range=xdr, y_range=ydr, plot_width=700, plot_height=400)

        xaxis = LinearAxis()
        plot.add_layout(xaxis, 'below')
        yaxis = LinearAxis(ticker=SingleIntervalTicker(interval=5))
        plot.add_layout(yaxis, 'left')

        plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

        male_quad = Quad(left="male", right=0, bottom="groups", top="shifted", fill_color="#3B8686")
        male_quad_glyph = plot.add_glyph(self._source_pyramid, male_quad)

        female_quad = Quad(left=0, right="female", bottom="groups", top="shifted", fill_color="#CFF09E")
        female_quad_glyph = plot.add_glyph(self._source_pyramid, female_quad)

        plot.add_layout(Legend(legends=[("Male", [male_quad_glyph]), ("Female", [female_quad_glyph])]))

        return plot


    def population_plot(self):
        xdr = FactorRange(factors=self._years)
        ydr = DataRange1d()

        plot = Plot(title=None, x_range=xdr, y_range=ydr, plot_width=700, plot_height=200,name='bk-population')

        plot.add_layout(CategoricalAxis(major_label_orientation=pi/4), 'below')

        line_known = Line(x="x", y="y", line_color="violet", line_width=2)
        line_known_glyph = plot.add_glyph(self._source_known, line_known)

        line_predicted = Line(x="x", y="y", line_color="violet", line_width=2, line_dash="dashed")
        line_predicted_glyph = plot.add_glyph(self._source_predicted, line_predicted)

        plot.add_layout(
            Legend(
                location="bottom_right",
                legends=[("known", [line_known_glyph]), ("predicted", [line_predicted_glyph])],
            )
        )

        return plot

    def update_pyramid(self):
        self._pyramid = self._df[(self._df.Location == self._location) & (self._df.Year == self._year)]

        male = self._pyramid[self._pyramid.Sex == "Male"]
        female = self._pyramid[self._pyramid.Sex == "Female"]

        total = male.Value.sum() + female.Value.sum()

        male_percent = -male.Value/total
        female_percent = female.Value/total

        groups = male.AgeGrpStart.tolist()
        shifted = groups[1:] + [groups[-1] + 5]

        self._source_pyramid.data = dict(
            groups=groups,
            shifted=shifted,
            male=male_percent,
            female=female_percent,
        )
        #print (source_pyramid.data)

    def update_population(self):
        self._population = self._df[self._df.Location == self._location].groupby(self._df.Year).Value.sum()
        aligned_revision = self._revision//10 * 10

        known = self._population[self._population.index <= aligned_revision]
        predicted = self._population[self._population.index >= aligned_revision]

        self._source_known.data = dict(x=known.index.map(str), y=known.values)
        self._source_predicted.data = dict(x=predicted.index.map(str), y=predicted.values)

    def update_data(self):
        self.update_population()
        self.update_pyramid()

    def change_year(self,new):
        self._year = int(new)
        self.update_data()

    def on_year_change(self,attr, old, new):
        self._year = int(new)
        self.update_data()

    def on_location_change(self,attr, old, new):
        self._location = new
        self.update_data()

    def plots(self):
        #controls = row(children=[year_select, location_select])
        #layout = column(children=[controls, pyramid(), population()])
        #layout = column(children=[self._pyramid_plot, self.population_plot()],sizing_mode="fixed", responsive=False)
        layout = column(children=[self.population_plot()],sizing_mode="fixed", responsive=False)

        return layout

    def header(self):
        year_select = Select(title="Year:", value="2010", options=self._years,width=80,name="year_select")
        location_select = Select(title="Location:", value="World", options=self._locations,width=600)
        #print (year_select.name)

        year_select.on_change('value', self.on_year_change)
        location_select.on_change('value', self.on_location_change)

        controls = row(children=[year_select, location_select])
        layout = column(children=[controls],sizing_mode="fixed", name="header")

        return layout

    def layout(self):
        print("Add Layout")
        return layout([[self.header()],[self.plots()]])
        #return layout([[self.header()]])

population = Population(name='bk-classdemo')
curdoc().add_root(population)
curdoc().title = "Population"
#if __name__ == "__main__":
        #print("\npress ctrl-C to exit")
        #session.loop_until_closed()
