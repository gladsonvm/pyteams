from functools import wraps


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
        self.__init__(*args, **kwargs)
        if hasattr(self, 'user') and self.user is not None:
            self.permission_bypass_flag = kwargs.get('permission_bypass_flag', None)
            if self.permission_bypass_flag == 'group' or self.permission_bypass_flag is None:
                if self.user.has_perm('pyteams.add_team'):
                    return method(self, *args, **kwargs)
                raise PermissionException('Assign Permission pyteams.add_team to User object that corresponds to '
                                          'current user. Use admin interface to assign permissions.')
            if self.permission_bypass_flag == 'user':
                try:
                    group = self.user.groups.get(name='manager')
                    group.permissions.get(codename='add_team')
                    return method(self, *args, **kwargs)
                except:
                    raise PermissionException('create manager group and assign permission add_team. '
                                              'Use admin interface to assign permissions.')
        return {'status': 400, 'description': 'User object is mandatory for create_team() '
                                              'unless permission_bypass_flag is set to True'}
    return wrapper


class PermissionException(Exception):
    pass


class TypeException(Exception):
    pass
