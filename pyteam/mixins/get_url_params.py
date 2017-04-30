class ExtractUrlParams(object):
    """
    Insert Plugin object to kwargs dict of view.
    plugin_type and plugin_name are extracted from url kwargs.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)
