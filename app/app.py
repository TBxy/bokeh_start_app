# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template

import commands, public, user, plots, admin
from .assets import assets
from .extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate, api, flask_admin
from .settings import ProdConfig
#from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from api.v1 import *



def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    login_manager.anonymous_user = user.models.AnonymousUser
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    flask_admin.init_app(app, index_view=admin.views.MyAdminIndexView())
    flask_admin.add_view(admin.views.UsersAdmin(user.models.User, db.session, endpoint='admin_users'))
    flask_admin.add_view(admin.views.RolesAdmin(user.models.Roles, db.session))
    #flask_admin.add_view(ModelView(user.models.UserRoles, db.session))
    flask_admin.add_view(admin.views.PermissionsAdmin(user.models.Permissions, db.session))
    flask_admin.add_link(MenuLink(name='Back Home', url='/'))


    #assets.url_expire = True

    return None


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(plots.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 403, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
    app.cli.add_command(commands.insertdb)
