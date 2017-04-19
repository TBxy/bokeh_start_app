# -*- coding: utf-8 -*-
"""User models."""
from __future__ import print_function

import bokeh.embed as bkembed
import bokeh.util as bkutil
import bokeh.client as bkclient
import bokeh.plotting as bkplt
import bokeh.models as bkmod
import bokeh.charts as bkcharts
import bokeh.resources as bkres
import bokeh as bk

from flask import request

class API_Source_Plot():
    """A simple plot which uses a server as source."""

    def __init__(self, title="Sine Plot", data_url=None , interval=0, plot="line"):
        """Create instance."""
        self.data_url = request.url_root + "api/v1/example" if not data_url else data_url
        self.title = title
        self.interval = interval
        self.plot = plot
        print("Created a api plot with title {}".format(title))

    def layout(self):
        source = bkmod.AjaxDataSource(data_url=self.data_url, \
                                polling_interval=self.interval, mode='replace', method="GET")
        callback = bkmod.CustomJS(args=dict(source=source), code="""
            //console.log(source);
            var name = cb_obj.attributes.name
            if(name == "fs"){{ source.fs = cb_obj.value }}
            if(name == "f"){{ source.f = cb_obj.value }}
            // set default value
            var fs = (typeof source.fs === 'undefined') ? 1000 : source.fs;
            var f = (typeof source.f === 'undefined') ? 5 : source.f;
            source.data_url = "{}/"+fs+"/"+f;
            source.get_data('replace');
        """.format(self.data_url))

        slider_fs = bkmod.widgets.Slider(start=100, end=2000, value=1000, step=50, name="fs", callback=callback)
        slider_f = bkmod.widgets.Slider(start=1, end=20, value=5, step=1, name="f", callback=callback)
        #button = bkmod.widgets.Button(label="Update", button_type="success",callback=callback, name="update")
        #streaming=True

        source.data = dict(x=[], yn=[], y=[])

        fig = bkplt.figure(title="Streaming Example")
        if self.plot == "line":
            fig.line('x','y', source=source, legend="sine", \
                    line_color="orange", line_width=4)
            fig.line( 'x', 'yn', legend="sine noise", alpha= 0.1, source=source)
        if self.plot == "scatter":
            fig.line('x','y', source=source, legend="sine", \
                    line_color="orange", line_width=4)
            fig.scatter( 'x', 'yn', legend="sine noise", alpha= 0.05, source=source)

        script, div = bkembed.components(bk.layouts.layout([[slider_fs,slider_f],\
                        [fig]], responsive=False, sizing_mode="scale_width")\
                , bkres.INLINE)

        plot = { "title" : self.title,
                "plot" : div,
                "script" : script }
        return plot

        #html = template.render(
            #plot_script=script,
            #plot_div=div,
            #js_resources=js_resources,
            #css_resources=css_resources
        #)


