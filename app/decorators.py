from functools import wraps
from werkzeug.exceptions import Forbidden


def _import_user():
    try:
        from flask_login import current_user
        return current_user
    except ImportError:
        raise ImportError(
            'User argument not passed and Flask-Login current_user could not be imported.')


def user_has(permission, get_user=_import_user):
    """
    Takes a permission (a string name) and returns the function if the user has that permission
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = get_user()
            if current_user.has(permission):
                return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper


def user_is(role, get_user=_import_user):
    """
    Takes a role (a string name) and returns the function if the user has that role
    """
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_user = get_user()
            if current_user.has_role(role):
                return func(*args, **kwargs)
            raise Forbidden("You do not have access")
        return inner
    return wrapper
