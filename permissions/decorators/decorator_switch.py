from api.mappings.permissions.permission_decorators import permission_decorator_mappings


def check_perms_fetch_object(func):

    def wrapper(instance, request, *args, **kwargs):
        handle, permission_decorator = None, None
        handle = permission_decorator_mappings.get('handles').get(kwargs.get('handle'))
        if handle:
            permission_decorator = handle.get('actions').get(kwargs.get('method'))
            if permission_decorator:
                return permission_decorator(func)(instance, request, *args, **kwargs)
        if handle is None or permission_decorator is None:
            kwargs.update({'response': {
                'error': 'handler/method/method permission not found. hit '
                'http://localhost:8000/info?endpoint=/handler/method/&type=permissions '
                         'to get a list of available handler-method permissions'
            }})
            return func(instance, request, *args, **kwargs)
    return wrapper
