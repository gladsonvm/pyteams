from functools import wraps
from .utils import validate_arguments


def set_class_attrs(method, *args, **kwargs):
    """
    This method set attributes to TeamHandler class
    :param method: method of TeanHandler class
    :param args: args required to trigger method
    :param kwargs: optional args
    :return: method if attributes are set successfully else error as Json message.
    """
    @wraps(method, *args, **kwargs)
    def wrapper(self, *args, **kwargs):
        if method.func_name == 'create_team':
            is_valid = validate_arguments(method.func_name, *args, **kwargs)
            if isinstance(is_valid, tuple):
                self.team_name = args[0] if is_valid[1] == 'args' else kwargs.get('team_name')
                self.team_type = args[1] if is_valid[1] == 'args' else kwargs.get('team_type')
                self.user = args[2] if is_valid[1] == 'args' else kwargs.get('team_type')
                self.description = args[3] if is_valid[1] == 'args' else kwargs.get('description')
            else:
                return {'status': 400, 'description': 'Validation Failed. Provide parameters in the order '
                        '({}, {}, {}, {})'.format('team_name', 'team_type', 'created_by', 'description')}
        if method.func_name == 'retrieve_team':
            is_valid = validate_arguments(method.func_name, *args, **kwargs)
            if isinstance(is_valid, tuple):
                self.user = args[0] if len(args) else kwargs.get('user')
                self.members = args[1] if len(args) == 2 else kwargs.get('members')
            else:
                return {'status': 400, 'description': 'Validation Failed. Provide parameters in the order '
                        '({}, {})'.format('user', '[members]')}
    return wrapper


def permission_bypass(method, *args, **kwargs):
    """
    This method is used as a decorator to check if user/group have proper permissions to create a Team object.
    self.__init__() is called to assign values to class variables at once.
    :param method: method that is passed as an input to this decorator
    :param args: class variables in the order (team_name, team_type, created_by, description).
    :param kwargs: optional arguments. Accepted names are same as name of args.
    :return: method if user or group have proper permissions else Exceptions are raised. If args/kwargs
    are not passed in predefined order, then a dict is returned with error code 400 and proper description.
    """
    @wraps(method, *args, **kwargs)
    def wrapper(self, *args, **kwargs):
        if self.permission_bypass_flag is True:
            return method(self, *args, **kwargs)
        if hasattr(self, 'user') and self.user is not None:
            self.permission_bypass_flag = kwargs.get('permission_bypass_flag', None)
            if self.permission_bypass_flag == 'group' or self.permission_bypass_flag is None:
                if self.user.has_perm('pyteams.add_team'):
                    return method(self)
                raise PermissionException('Assign Permission pyteams.add_team to User object that corresponds to '
                                          'current user. Use admin interface to assign permissions.')
            if self.permission_bypass_flag == 'user':
                try:
                    group = self.user.groups.get(name='manager')
                    group.permissions.get(codename='add_team')
                    return method(self)
                except:
                    raise PermissionException('create manager group and assign permission add_team. '
                                              'Use admin interface to assign permissions.')
            return {'status': 400, 'description': 'User object is mandatory for create_team()'
                                                  ' unless permission_bypass_flag is set to True'}
        return {'status': 400, 'description': 'user identifier must be an object of type User'}
    return wrapper


class PermissionException(Exception):
    pass


class TypeException(Exception):
    pass
