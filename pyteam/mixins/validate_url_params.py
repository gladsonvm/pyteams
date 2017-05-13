from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from api.mappings.handler_mappings import handler_method_mappings
from permissions.decorators.decorator_switch import check_perms_fetch_object

msg = 'hit /info?endpoint=/handler/method/&type=permissions to get ' \
      'a list of available handler-method mappings'


class ValidateUrlParams(object):
    """
    validate params passed from url to views.
    """
    # declare handle and method as class variables to access it in views.
    handle = None
    method = None

    @method_decorator(csrf_exempt)
    @check_perms_fetch_object
    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        if kwargs.get('response') is None:
            if kwargs.get('handle') in handler_method_mappings.keys():
                self.handle = kwargs.get('handle')
                if kwargs.get('method') in handler_method_mappings.get(kwargs.get('handle')):
                    self.method = kwargs.get('method')
                    if request.method.lower() in self.http_method_names:
                        handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
                    else:
                        handler = self.http_method_not_allowed
                    return handler(request, *args, **kwargs)
                return JsonResponse({'error': 'method not found for given handler. '+msg}, status=404)
            return JsonResponse({'error': 'handler not found. '+msg}, status=404)
        if hasattr(kwargs.get('response'), 'status_code') and kwargs.get('response').status_code == 403:
            return JsonResponse({'error': 'permission denied'}, status=403)
        return kwargs.get('response')
