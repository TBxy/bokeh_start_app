# coding: utf-8
# pylint: disable=too-few-public-methods, no-self-use, missing-docstring, unused-argument
from flask_restful import Resource
import numpy as np
from ...extensions import api
from ...utils import bokeh_app_url

import bokeh.client as bkclient



"""
Provides API example
"""
#@api.resource('param/<session_id>/<app>/<key>')
@api.resource('param/<session_id>/<app>/<key>/<value>')
class AppParam(Resource):
    """Changes an single value in a source object in a bokeh app.
    This value information can be changed via ajax calls.

    The following needs to be added to a bokeh app:

    from bokeh.io import curdoc
    from bokeh.models import ColumnDataSource
    app_param = ColumnDataSource(data={'key1':["value1"],
                                       'key2':["value2"]},
                                        name="app_param")

    def update_app_params(attr, old, new):
        key1 = int(new['key1'][0])
        key2 = str(new['key2'][0])
        # do something with the new data

    curdoc().add_root(app_param)
    app_param.on_change('data', update_app_params)

    """
    def get(self,session_id=None,app=None, key=None, value=None):
        app_param_name = 'app_param' # should be possible to change by request parameter
        session = bkclient.pull_session(session_id=session_id, url=bokeh_app_url(app))
        app_param =session.document.get_model_by_name(app_param_name)
        # as soon we change data from app_param the plot is updated
        if value != None:
            app_param.data[key] = [value]
        else:
            value = app_param.data[key]
        return {'status' : 200,
                'id' : session.id,
                key : value,
                'key' : key,
                'value' : value
            }


"""
Provides API example
"""
@api.resource('plots/function-plotter/<id>/<function>','example')
class FunctionPlotterAPI(Resource):
    """Gets list of users. Uses ndb Cursor for pagination. Obtaining users is executed
    in parallel with obtaining total count via *_async functions
    """
    def get(self,id=None,function=""):
        app_name = 'function_plotter'
        session = bkclient.pull_session(session_id=id, app_path='/'+app_name)
        print(session.request_server_info())
        model =session.document.get_model_by_name('bk-function-plotter')
        #model.change_function(function)
        model.source.data = {'x' : [10,20],
                            'y' : [5,7]}

        #session.push()
        x = model.source.data['x']
        y = model.source.data['y']
        try:
            x = x.tolist()
            y = y.tolist()
        except:
            pass
        return {'status' : 200,
                'id' : session.id,
                'function' : model.function,
                'x' : x,
                'y' : y
            }



"""
Provides API example
"""
@api.resource('plots/population/update/<id>/<year>/<location>','example')
class PopulationUpdateAPI(Resource):
    """Gets list of users. Uses ndb Cursor for pagination. Obtaining users is executed
    in parallel with obtaining total count via *_async functions
    """
    def get(self,id=None,year="2015", location="World"):
        app_name = 'population'
        session = bkclient.pull_session(session_id=id, url=bokeh_app_url('population'))
        print(session.request_server_info())
        app_param =session.document.get_model_by_name("app_param")
        # as soon we change data from app_param the plot is updated
        app_param.data['year'] = [year]
        app_param.data['location'] = [location]
        return {'status' : 200,
                'id' : session.id,
                'year' : year,
                'location' : location
            }

