# coding: utf-8
# pylint: disable=too-few-public-methods, no-self-use, missing-docstring, unused-argument
from flask_restful import Resource
import numpy as np
from ...extensions import api

import bokeh.client as bkclient
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

