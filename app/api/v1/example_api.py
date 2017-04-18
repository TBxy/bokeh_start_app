# coding: utf-8
# pylint: disable=too-few-public-methods, no-self-use, missing-docstring, unused-argument
from flask_restful import Resource
import numpy as np
from ...extensions import api
"""
Provides API example
"""
@api.resource('example/<int:fs>/<int:f>','example')
class ExampleAPI(Resource):
    """Gets list of users. Uses ndb Cursor for pagination. Obtaining users is executed
    in parallel with obtaining total count via *_async functions
    """
    def get(self,fs=1000,f=5, n=0.2):
        sample = 10000
        x = np.arange(sample)
        y = np.sin(2 * np.pi * f * x / fs)
        noise = np.random.randn(sample) * n + 1
        yn = y * noise
        return {'x' : x.tolist(),
                'yn' : yn.tolist(),
                'y' : y.tolist()}

