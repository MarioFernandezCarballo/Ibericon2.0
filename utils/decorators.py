from functools import wraps

from flask_login import current_user


##############
# Decorators #
def only_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 15:
            return func(*args, **kwargs)
    return decorated_view


def only_right_hand(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 14:
            return func(*args, **kwargs)
    return decorated_view


def only_left_hand(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 13:
            return func(*args, **kwargs)
    return decorated_view


def only_collaborator(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 12:
            return func(*args, **kwargs)
    return decorated_view


def only_tournament_organizer(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 11:
            return func(*args, **kwargs)
    return decorated_view


def only_team_leader(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 10:
            return func(*args, **kwargs)
    return decorated_view


def only_adamantium(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 4:
            return func(*args, **kwargs)
    return decorated_view


def only_diamantite(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 3:
            return func(*args, **kwargs)
    return decorated_view


def only_ceramite(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 2:
            return func(*args, **kwargs)
    return decorated_view


def only_plasteel(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 1:
            return func(*args, **kwargs)
    return decorated_view
