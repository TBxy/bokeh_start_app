# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
import re
from flask import flash, request


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)


def bokeh_app_url(app_name=""):
    # replace port :XXXX with :5006 (bokeh port)
    url = re.sub(":\d{4}",":5006", request.url_root)
    return url + app_name
