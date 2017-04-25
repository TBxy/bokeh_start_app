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
#from __future__ import print_function

from numpy import pi

from bokeh.client import push_session
from bokeh.document import Document
from bokeh.io import curdoc
from bokeh.embed import autoload_server
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.models import (Plot, DataRange1d, LinearAxis, CategoricalAxis,
                          Legend, ColumnDataSource, Grid, Line,
                          SingleIntervalTicker, Quad, Select, FactorRange)
from bokeh.sampledata.population import load_population
from bokeh.server.events import TitleChangedEvent



df = load_population()
revision = 2012

years = [str(x) for x in sorted(df.Year.unique())]
locations = sorted(df.Location.unique())

# parameters for the data
# this can also be changed from external
app_param = ColumnDataSource(data={'year':["2015"],
                                      'location' : ["World"]},
                                       name="app_param")

source_pyramid = ColumnDataSource(data=dict(), name="source_pyramid")
def pyramid():
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
    male_quad_glyph = plot.add_glyph(source_pyramid, male_quad)

    female_quad = Quad(left=0, right="female", bottom="groups", top="shifted", fill_color="#CFF09E")
    female_quad_glyph = plot.add_glyph(source_pyramid, female_quad)

    plot.add_layout(Legend(legends=[("Male", [male_quad_glyph]), ("Female", [female_quad_glyph])]))

    return plot

source_known = ColumnDataSource(data=dict(x=[], y=[]),
        name="source_known")
source_predicted = ColumnDataSource(data=dict(x=[], y=[]),
        name="source_predicted")

def population():
    xdr = FactorRange(factors=years)
    ydr = DataRange1d()

    plot = Plot(title=None, x_range=xdr, y_range=ydr, plot_width=700, plot_height=200)

    plot.add_layout(CategoricalAxis(major_label_orientation=pi/4), 'below')

    line_known = Line(x="x", y="y", line_color="violet", line_width=2)
    line_known_glyph = plot.add_glyph(source_known, line_known)

    line_predicted = Line(x="x", y="y", line_color="violet", line_width=2, line_dash="dashed")
    line_predicted_glyph = plot.add_glyph(source_predicted, line_predicted)

    plot.add_layout(
        Legend(
            location="bottom_right",
            legends=[("known", [line_known_glyph]), ("predicted", [line_predicted_glyph])],
        )
    )

    return plot

def update_pyramid():
    location = app_param.data['location'][0]
    year = int(app_param.data['year'][0])
    pyramid = df[(df.Location == location) & (df.Year == year)]

    male = pyramid[pyramid.Sex == "Male"]
    female = pyramid[pyramid.Sex == "Female"]

    total = male.Value.sum() + female.Value.sum()

    male_percent = -male.Value/total
    female_percent = female.Value/total

    groups = male.AgeGrpStart.tolist()
    shifted = groups[1:] + [groups[-1] + 5]

    source_pyramid.data = dict(
        groups=groups,
        shifted=shifted,
        male=male_percent,
        female=female_percent,
    )

def update_population():
    location = app_param.data['location'][0]
    population = df[df.Location == location].groupby(df.Year).Value.sum()
    aligned_revision = revision//10 * 10

    known = population[population.index <= aligned_revision]
    predicted = population[population.index >= aligned_revision]

    source_known.data = dict(x=known.index.map(str), y=known.values)
    source_predicted.data = dict(x=predicted.index.map(str), y=predicted.values)

def update_data():
    update_population()
    update_pyramid()

def on_year_change(attr, old, new):
    app_param.data['year'] = [int(new)]

def on_location_change(attr, old, new):
    app_param.data['location'] = [new]

def plots():
    layout = column(children=[pyramid(), population()],sizing_mode="fixed", responsive=False)
    return layout

def header():
    global location_select, year_select
    year_select = Select(title="Year:", value="2010", options=years,width=80,name="year_select")
    location_select = Select(title="Location:", value="World", options=locations,width=600,name="location_select")

    year_select.on_change('value', on_year_change)
    location_select.on_change('value', on_location_change)

    controls = row(children=[year_select, location_select])
    layout = column(children=[controls],sizing_mode="fixed", name="header")

    return layout

def update_app_params(attr, old, new):
    global location_select, year_select
    location_select.value = new['location'][0]
    year_select.value = str(new['year'][0])
    update_data()

plots = plots()
header = header()

update_data()

doc = curdoc()
args = curdoc().session_context.request.arguments
if 'header' in args:
    doc.add_root(layout([[header],[plots]]))
else:
    doc.add_root(layout([[plots]]))
doc.add_root(app_param) # needs to be added to the document
app_param.on_change('data', update_app_params)

doc.title = "Population"
