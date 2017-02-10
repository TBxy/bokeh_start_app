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



from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from bokeh_start_app.extensions import login_manager
from bokeh_start_app.public.forms import LoginForm
from bokeh_start_app.user.forms import RegisterForm
from bokeh_start_app.user.models import User
from bokeh_start_app.utils import flash_errors

# Register blueprint in app.py
blueprint = Blueprint('public-plots', __name__, static_folder='../static')

import bokeh.embed as bkembed
import bokeh.util as bkutil

@blueprint.route('/plot1/')
def bokeh_plot():
    """About page."""
    form = LoginForm(request.form)
    id =  bkutil.session_id.generate_session_id(signed=True)
    print ("Session id is: {}".format(id))
    html = """
    <h2> This plots shows an animated fourier series</h2>
    <p> The plot is served from a bokeh server <p>
           <div id="fourier">
               {F}
           </div>
     """.format(F=bkembed.autoload_server(model=None,
                         session_id=id,
                         app_path="/fourier_animated"))
    plot = {}
    plot["plot1"] = html
    return render_template('public/plot_demo.html', form=form, plot=plot)
