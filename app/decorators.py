from functools import wraps
from flask import session, flash, redirect
from app import user_controller


def login_required(func_to_wrap):
    @wraps(func_to_wrap)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func_to_wrap(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect('/signin')
    return wrap


def requires_roles(*roles):
    def wrapper(func_to_wrap):
        @wraps(func_to_wrap)
        def wrapped(*args, **kwargs):
            if user_controller.get_current_user_role(session['user_id']) not in roles:
                return ('Not authorized', 401)
            else:
                return func_to_wrap(*args, **kwargs)
        return wrapped
    return wrapper
