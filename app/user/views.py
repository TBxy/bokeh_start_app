# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required
from ..decorators import user_has
blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')

#@login_required

@blueprint.route('/')
@user_has('view')
def members():
    """List members."""
    #print current_user
    return render_template('users/members.html')
