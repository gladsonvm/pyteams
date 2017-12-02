import json
from core.validators.rules import get_mandatory_param, get_validation_rule, get_all_params
from django.http import JsonResponse


class RequestDataValidatorMixin(object):
    """
    This class bounds all methods necessary to validate request data and provide a formatted output
    """
    def dispatch(self, request, *args, **kwargs):
        """
        overriding django's own dispatch to perform pluggable validation.
        :param request: WSGI request
        :param args: url args
        :param kwargs: url kwargs
        :return: http method if validation passes else validation error message.
        """
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        validation_response = self._validate_request_data(request)
        if validation_response[0] is False:
            return JsonResponse(validation_response[1], status=400)
        return handler(request, *args, **kwargs)

    def _validate_request_data(self, request):
        """
        This method provide formatted data after successful validation.
        :param request: WSGI request.
        :return: None if validation passes if any one validation fails, then appropriate error msg.
        """
        validators = [self._validate_request_body, self._validate_mandatory_params, self._validate_params]
        for validator in validators:
            if validator(request)[0]:
                pass
            else:
                return validator(request)
        return True,

    def _validate_mandatory_params(self, request):
        """
        This method checks if all mandatory params are there in a given json.
        :param request: WSGI request
        :return: False and error msg if validation fails else True.
        """
        self.rule = get_validation_rule(self, request.method.lower())
        mandatory_params = get_mandatory_param(self.rule)
        if mandatory_params:
            if len([x for x in [*mandatory_params] if x not in [*self.data]]):
                return False, {'error': 'mandatory params missing. mandatory parameters are {mandatory_params}'
                                        .format(mandatory_params=mandatory_params)}
        return True,

    def _validate_request_body(self, request):
        """
        This method checks if a given request body is a valid json.
        :param request: WSGI request
        :return: False and error msg if validation fails else True.
        """
        try:
            self.data = json.loads(request.body.decode('UTF-8'))
        except:
            return False, {'error': 'provide a valid json.'}
        return True,

    def _validate_params(self, request):
        """
        check if any invalid params are in request body.
        :param request: WSGI request.
        :return: False and error msg if validation fails else True.
        """
        allowed_params = get_all_params(self, request.method.lower())
        sorted_request_params = sorted([*self.data])
        sorted_allowed_params = sorted(allowed_params)
        invalid_params = [x for x in sorted_request_params if x not in sorted_allowed_params]
        if invalid_params:
            return False, {'error': 'invalid params found in request body. invalid parameters are {invalid_params}'
                .format(invalid_params=invalid_params)}
        return True,
