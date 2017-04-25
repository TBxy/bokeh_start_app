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


from .api_source import API_Source_Plot



from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

#from ..extensions import login_manager
from ..public.forms import LoginForm
#from ..user.forms import RegisterForm
#from ..user.models import User
#from ..utils import flash_errors

# Register blueprint in app.py
blueprint = Blueprint('plots', __name__, static_folder='../static')

import bokeh.embed as bkembed
import bokeh.util as bkutil
import bokeh.client as bkclient
#import bokeh.plotting as bkplt
#import bokeh.models as bkmod
#import bokeh.resources as bkres
#import bokeh as bk

#from bokeh.resources import INLINE
#from bokeh.util.string import encode_utf8

from ..utils import bokeh_app_url

from bokeh.sampledata.population import load_population


def PLOTS_SUBNAV():
    return [{"name" : "Fourier", "url" : url_for('plots.fourier'),
                "icon" : None, "has_role" : None, "permission":  "view"},
        {"name" : "Population", "url" : url_for('plots.population_plot'),
                "has_role" : None, "permission" : "view"},
        {"name" : "Movies", "url" : url_for('plots.movies'),
                "has_role" : None, "permission" : "view"},
        {"name" : "Sine (api)", "url" : url_for('plots.bokeh_apiplot'),
                "has_role" : None, "permission" : "view"},
        #{"name" : "Population Class", "url" : url_for('plots.population_class_plot'),
                #"has_role" : "admin", "permission" : "view"},
        {"name" : "Function Plotter", "url" : url_for('plots.function_plotter'),
                "has_role" : None, "permission" : "view"}]


@blueprint.route('/fourier/')
def fourier(title="Default"):
    """About page."""
    login_form = LoginForm(request.form)
    html = """<div id="fourier">
               {F}
           </div>
     """.format(F=bkembed.autoload_server(model=None,
                         url=bokeh_app_url('fourier_animated')))
    plot = {"plot1" : html}
    return render_template('public/plot_demo.html', form=login_form, plot=plot, subnav=PLOTS_SUBNAV())



@blueprint.route('/apiplot/')
def bokeh_apiplot(title="Default"):
    """About page."""
    form = LoginForm(request.form)
    plots = []
    plots.append(API_Source_Plot(title="Sine One"))
    plots.append(API_Source_Plot(title="Sine Two",plot='scatter'))
    plots.append(API_Source_Plot(title="Sine Three",plot='line'))
    return render_template('public/simple_plot.html', form=form, plots=[p.layout() for p in plots], subnav=PLOTS_SUBNAV())


@blueprint.route('/population/')
@blueprint.route('/population/<year>')
@blueprint.route('/population/<year>/<location>')
def population_plot(title="Default",year="2015", location="World"):
    """About page."""
    login_form = LoginForm(request.form)
    id =  bkutil.session_id.generate_session_id(signed=True)
    session = bkclient.pull_session(session_id=id, url=bokeh_app_url('population'))
    print ("Session id is: {}".format(session.id))
    app_param =session.document.get_model_by_name("app_param")
    # as soon we change data from app_param the plot is updated
    app_param.data['year'] = [year]
    app_param.data['location'] = [location]
    html = """
           <div id="population-plot">
               {F}
           </div>
     """.format(F=bkembed.autoload_server(model=None,
                         session_id=session.id,
                         url=bokeh_app_url('population')))
    plot = {"plot1" : html}
    df = load_population()
    years = [str(x) for x in sorted(df.Year.unique())]
    locations = sorted(df.Location.unique())
    return render_template('public/population_plot.html', form=login_form, plot=plot, subnav=PLOTS_SUBNAV(), session_id=id, years=years, default_year=year,locations=locations, default_location=location)

@blueprint.route('/movies/')
def movies(title="Default"):
    """About page."""
    login_form = LoginForm(request.form)
    id =  bkutil.session_id.generate_session_id(signed=True)
    session = bkclient.pull_session(session_id=id, url=bokeh_app_url('movies'))
    app_param =session.document.get_model_by_name("app_param")
    # as soon we change data from app_param the plot is updated
    #app_param.data['year'] = [year]
    html = """
           <div id="movies-plot">
               {F}
           </div>
     """.format(F=bkembed.autoload_server(model=None,
                         session_id=session.id,
                         url=bokeh_app_url('movies')))
    plot = {"plot1" : html}
    return render_template('public/movies_plot.html', form=login_form, plot=plot, subnav=PLOTS_SUBNAV(), session_id=id)



@blueprint.route('/population-class/')
@blueprint.route('/population-class/<int:year>')
def population_class_plot(title="Default",year=0):
    """About page."""
    form = LoginForm(request.form)
    id =  bkutil.session_id.generate_session_id(signed=True)
    session = bkclient.pull_session(session_id=id, url=bokeh_app_url('population_class'))
    print ("Session info:")
    #print (session.request_server_info())
    print ("Session id is: {}".format(session.id))
    mypy =session.document.get_model_by_name('bk-pyramid')
    mypop =session.document.get_model_by_name('bk-population')
    mymodel =session.document.get_model_by_name('bk-classdemo')
    print ("Model bk-pyramid")
    print (mypy)
    print ("Model bk-population")
    print (mypop)
    print ("Model bk-classdemo")
    print (mymodel)
    html = """
           <div id="population-class-plot">
               {F}
           </div>
     """.format(F=bkembed.autoload_server(model=None,
                         session_id=session.id,
                         url=bokeh_app_url('population_class')))

    plot = {}
    plot["plot1"] = html
    if year > 0:
        mymodel.change_year(year)
    return render_template('public/population_plot.html', form=form, plot=plot, subnav=PLOTS_SUBNAV())


@blueprint.route('/function-plotter/<func>', methods=['GET', 'POST'])
@blueprint.route('/function-plotter/', methods=['GET', 'POST'])
def function_plotter(title="Default",func="sin(x)"):
    """About page."""
    #print ("REQUESTS:")
    #print (request.form)
    #print (request.args)
    #print (request)
    login_form = LoginForm(request.form)
    if request.method == 'POST':
        #print ("POST method:")
        #print (request)
        func = request.form['formula']
        start = request.form['start']
        end = request.form['end']
        points = request.form['points']
        return redirect(url_for('plots.function_plotter')+func)
    app_name = 'function_plotter'
    id =  bkutil.session_id.generate_session_id(signed=True)
    #session = bkclient.pull_session(session_id=id, url=bokeh_app_url(app_name))
    #print ("Session id is: {}".format(session.id))
    #model =session.document.get_model_by_name('bk-function-plotter')
    #print ("Model bk-function-plotter")
    #print (model)
    html = """
           <div id="population-class-plot">
               {F}
           </div>
     """.format(F=bkembed.autoload_server(model=None,
                         session_id=id,
                         #app_path="?f=cos(x)",
                         url=bokeh_app_url(app_name)))

    plot = {}
    plot["plot1"] = html
    #session.template_variables["fp"].change_function(func)
    #session.document.session_context['fp'].change_function(func)
    #print(session.document.roots)
    return render_template('public/function_plotter.html', form=login_form, plot=plot,session_id=id, subnav=PLOTS_SUBNAV())


