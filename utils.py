from flask import Response
from functools import wraps
from flask import request, session, flash
from . import server_constants, error_messages, InvalidUsage
import re
import json

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def return_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset=utf-8')
    return decorated_function

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if server_constants.session_key in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return json.dumps(error_messages.session_expired)
    return wrap

def is_valid_email(email):
    if not email:
        return False 
    return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))

def correct_phone(phone):
    
    return phone