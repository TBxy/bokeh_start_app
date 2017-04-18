# -*- coding: utf-8 -*-
"""Flask-Admin views."""
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose

from ..decorators import user_is

# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

    @expose('/')
    @user_is('admin')
    def index(self):
        #if not login.current_user.is_authenticated:
            #return redirect(url_for('.login_view'))
        return super(MyAdminIndexView, self).index()


class UsersAdmin(ModelView):
    """Flask user model view."""
    column_searchable_list = ('username', 'email')
    #column_editable_list = ['email', 'name','active']
    column_exclude_list = ('password')
    #create_modal = True
    edit_modal = True
    #column_hide_backrefs = False
    #can_view_details = True
    #form_columns = ['username', 'roles']
    #column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('username', 'email', 'name', 'active','is_admin','roles','created_at')

    def _on_model_change(self, form, User, is_created):
        if is_created or self._old_pw != form.password.data:
            User.set_password(form.password.data)


    def on_form_prefill(self, form, id):
        self._old_pw = form.password.data


class RolesAdmin(ModelView):
    """Flask user model view."""
    column_hide_backrefs = False
    column_list = ('name', 'permissions', 'description')

class PermissionsAdmin(ModelView):
    """Flask user model view."""
    column_hide_backrefs = False
    column_list = ('name', 'roles', 'description')
