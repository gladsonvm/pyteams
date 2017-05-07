from django.http import JsonResponse
from api.mappings.handler_mappings import handler_method_mappings
from permissions.decorators.decorator_switch import check_perms_fetch_object

class ValidateUrlParams(object):
    """
    validate params passed from url to views.
    """
    @check_perms_fetch_object
    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('handle') in handler_method_mappings.keys():
            if kwargs.get('method') in handler_method_mappings.get(kwargs.get('handle')):
                if request.method.lower() in self.http_method_names:
                    handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
                else:
                    handler = self.http_method_not_allowed
                return handler(request, *args, **kwargs)
            return JsonResponse({'error': 'method not implemented for handler'}, status=501)
        return JsonResponse({'error': 'handler not implemented.'}, status=501)

