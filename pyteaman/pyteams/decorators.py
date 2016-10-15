from functools import wraps
from .permissions import is_admin_or_manager
from .utils import get_user_on_user_identifier


def is_manager(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        user_identifier = kwargs.get('user_identifier') if kwargs.get('user_identifier') else args[0]
        user = get_user_on_user_identifier(user_identifier)
        if user:
            if is_admin_or_manager(user):
                return method(self, *args, **kwargs)
            else:
                return {'status': 403, 'description': 'Only Manager/Admin roles can create team.'}
        else:
            return {'status': 404, 'description': 'No user with given username/email exists.'}
    return wrapper

class PermissionException(Exception):
    pass