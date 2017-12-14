from functools import wraps
from flask import session, flash, redirect


def login_required(func_to_wrap):
    @wraps(func_to_wrap)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func_to_wrap(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect('/signin')
    return wrap
