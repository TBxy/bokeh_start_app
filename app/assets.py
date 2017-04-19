# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment



sass = Bundle('libs/materialize/sass/materialize.scss'
        , filters='pyscss', output='public/css/sass.css')
#all_css = Bundle('css/jquery.calendar.css', sass,
                 #filters='cssmin', output="gen/all.css")

css = Bundle(
    #'libs/bootstrap/dist/css/bootstrap.css',
    #'libs/materialize/dist/css/materialize.css',
    sass,
    'css/style.css',
    "css/bokeh-widgets.css",
    "css/bokeh.css",
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'libs/jQuery/dist/jquery.js',
    #'libs/bootstrap/dist/js/bootstrap.js',
    'libs/materialize/dist/js/materialize.js',
    'js/plugins.js',
    'js/script.js',
    "js/bokeh.js",
    "js/bokeh-gl.js",
    "js/bokeh-widgets.js",
    'libs/loglevel/dist/loglevel.js',
    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
