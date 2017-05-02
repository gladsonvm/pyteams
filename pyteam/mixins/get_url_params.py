from api.mappings.permissions.permission_decorators import permission_decorator_mappings


class ExtractUrlParams(object):
    """
    set permission required decorator and params for the same.
    """
    permission_req_decorator = None

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            permission_req_decorator = \
                permission_decorator_mappings.get('handles').get(kwargs.get('handle')).get('actions').get(kwargs.get('method'))
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            return permission_req_decorator(handler(request, *args, **kwargs))
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
