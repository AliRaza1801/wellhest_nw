from functools import wraps

from flask import current_app
from flask_login import current_user


def vendor_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.business_client:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view
# Change unauthorised callback after handling this


def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return current_app.login_manager.unauthorized()
    return decorated_view
