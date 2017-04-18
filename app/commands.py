# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound

import user
#from bokeh_start_app.extensions import db

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@click.command()
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose'])
    exit(rv)


@click.command()
@click.option('-f', '--fix-imports', default=False, is_flag=True,
              help='Fix imports using isort, before linting')
def lint(fix_imports):
    """Lint and check code style with flake8 and isort."""
    skip = ['requirements']
    root_files = glob('*.py')
    root_directories = [
        name for name in next(os.walk('.'))[1] if not name.startswith('.')]
    files_and_directories = [
        arg for arg in root_files + root_directories if arg not in skip]

    def execute_tool(description, *args):
        """Execute a checking tool with its arguments."""
        command_line = list(args) + files_and_directories
        click.echo('{}: {}'.format(description, ' '.join(command_line)))
        rv = call(command_line)
        if rv != 0:
            exit(rv)

    if fix_imports:
        execute_tool('Fixing import order', 'isort', '-rc')
    execute_tool('Checking code style', 'flake8')


@click.command()
def clean():
    """Remove *.pyc and *.pyo files recursively starting at current directory.

    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)


@click.command()
@click.option('--url', default=None,
              help='Url to test (ex. /static/image.png)')
@click.option('--order', default='rule',
              help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url, order):
    """Display all of the url matching routes for the project.

    Borrowed from Flask-Script, converted to use Click.
    """
    rows = []
    column_length = 0
    column_headers = ('Rule', 'Endpoint', 'Arguments')

    if url:
        try:
            rule, arguments = (
                current_app.url_map
                           .bind('localhost')
                           .match(url, return_rule=True))
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ''
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        # max_endpoint_length = max(rows, key=len)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    click.echo(str_template.format(*column_headers[:column_length]))
    click.echo('-' * table_width)

    for row in rows:
        click.echo(str_template.format(*row[:column_length]))

@click.command()
@with_appcontext
def insertdb():
    """Initialize app's DB with data."""
    #current_app.create_app().app_context().push()
    admin = user.models.User(username="admin", name="admin",
                email="admin", password="admin", is_admin=True, active=True)
    guest = user.models.User(username="guest", name="guest",
                email="guest", password="guest", active=True)
    anonymous = user.models.User(username="anonymous", name="anonymous",
                email="anonymous", password="anonymous", active=True)
    admin_role = user.models.Roles(name="admin")
    editor_role = user.models.Roles(name="editor")
    reader_role = user.models.Roles(name="reader")
    anonymous_role = user.models.Roles(name="anonymous",
            description="Role for unlogged users")
    write_perm = user.models.Permissions(name="write")
    view_perm = user.models.Permissions(name="view")
    delete_perm = user.models.Permissions(name="delete")
    edit_perm = user.models.Permissions(name="edit")
    create_perm = user.models.Permissions(name="create")
    # add permissions to roles
    admin_role.permissions.append(write_perm)
    admin_role.permissions.append(view_perm)
    admin_role.permissions.append(delete_perm)
    admin_role.permissions.append(edit_perm)
    admin_role.permissions.append(create_perm)
    editor_role.permissions.append(write_perm)
    editor_role.permissions.append(view_perm)
    editor_role.permissions.append(edit_perm)
    editor_role.permissions.append(create_perm)
    reader_role.permissions.append(view_perm)
    # add roles to user
    admin.roles.append(admin_role)
    guest.roles.append(reader_role)
    try:
        admin_role.save()
        editor_role.save()
        reader_role.save()
        anonymous_role.save()
        write_perm.save()
        view_perm.save()
        delete_perm.save()
        edit_perm.save()
        create_perm.save()
        admin.save()
        guest.save()
        anonymous.save()
    except Exception as e:
        print "ERROR while adding users"
        print e
        #print "user already added"
    #db.session.commit()
