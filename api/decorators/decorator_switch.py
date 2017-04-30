from api.mappings.permission_mappings import perm_mappings


def check_perms_fetch_object(func):

    def wrapper(instance, request, *args, **kwargs):
        permission_decorator = \
            perm_mappings.get('handles').get(kwargs.get('handle')).get('actions').get(kwargs.get('method'))
        return permission_decorator(func)(instance, request, *args, **kwargs)
    return wrapper
