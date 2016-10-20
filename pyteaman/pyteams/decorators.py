from functools import wraps
from .permissions import is_admin_or_manager
from .utils import get_user_on_user_identifier


def if_user_exists(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.user_identifier is None:
            self.user_identifier = args[2] if len(args) >= 3 else kwargs.get('created_by', None)
        if self.user_identifier:
            self.user = get_user_on_user_identifier(user_identifier=self.user_identifier)
            if self.user:
                return method(self, *args, **kwargs)
            if method.func_name == 'create_team':
                return {'status': 400, 'description': 'Provide parameters in the format {0}, {1}, {2}, {3}.'
                        .format('team_name', 'team_description', 'user_identifier', 'team_type')}
        return {'status': 404, 'description': 'No user with given user identifier exists.'}
    return wrapper


def is_manager(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.user:
            if is_admin_or_manager(self.user):
                return method(self, *args, **kwargs)
            else:
                return {'status': 403, 'description': 'Only Manager/Admin roles can create team.'}
        else:
            return {'status': 404, 'description': 'No user with given username/email exists.'}
    return wrapper


class PermissionException(Exception):
    pass

