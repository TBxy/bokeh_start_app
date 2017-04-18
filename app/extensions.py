# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app.py."""
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_restful import Api
from flask_admin import Admin
#from flask.ext.permissions.core import Permissions


bcrypt = Bcrypt()
csrf_protect = CsrfProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
api = Api(prefix="/api/v1/")
flask_admin = Admin(name='Starter App', template_mode='bootstrap3')
