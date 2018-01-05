import json
from django.http import JsonResponse, HttpResponse
from operator import attrgetter
from response.response import Response
from django.views.generic import View
from django.utils import six
from django.core import serializers

class RequestDataValidatorMixin(View):
    """
    This class bounds all methods necessary to validate request data and provide a formatted output
    """
    error_dict = dict()

    # def __init__(self, **kwargs):
    #     """
    #     init only if model and validation rule are provided in inherited class.
    #     """
    #     super(RequestDataValidatorMixin, self).__init__()
    #     for key, value in six.iteritems(kwargs):
    #         setattr(self, key, value)
    #     import ipdb;ipdb.set_trace()
    #     if not hasattr(self, 'model'):
    #         raise Exception("{class_name} must specify a model".format(class_name=type(self).__name__))
    #     if not hasattr(self, 'validation_rule'):
    #         raise Exception("{class_name} must specify a validation rule".format(class_name=type(self).__name__))
    #     self.request_body = self.request.body.decode('UTF-8')

    def validate_request_data(self):
        """
        This method is the entry point for provide formatted data after successful validation.
        :param request: WSGI request.
        :return: None if validation passes if any one validation fails, then appropriate error msg.
        """
        validators = [self.validate_request_body, self.validate_mandatory_params, self.validate_allowed_params]
        if hasattr(self, 'validators'):
            if type(self.validators) is list:
                validators = validators + self.validators
            else:
                raise TypeError('Validators provided in %s must be a list', self.__class__.__name__)

        for validator in validators:
            validation_result = validator()
            if validation_result[0]:
                pass
            else:
                self.error_dict.update(validation_result[1])
                return False
        return True

    def validate_mandatory_params(self):
        """
        This method checks if all mandatory params are there in a given json.
        :param request: WSGI request
        :return: False and error msg if validation fails else True.
        """
        mandatory_params = self.get_mandatory_param()
        if mandatory_params:
            if len([x for x in [*mandatory_params] if x not in [*self.data]]):
                return False, {'error': 'mandatory params missing. mandatory parameters are {mandatory_params}'
                                        .format(mandatory_params=mandatory_params)}
        return True,

    def validate_request_body(self):
        """
        This method checks if a given request body is a valid json.
        :param request: WSGI request
        :return: False and error msg if validation fails else True.
        """
        try:
            self.data = json.loads(self.request.body.decode('UTF-8'))
        except:
            return False, {'error': 'provide a valid json.'}
        return True,

    def validate_allowed_params(self):
        """
        check if any invalid params are in request body.
        :param request: WSGI request.
        :return: False and error msg if validation fails else True.
        """
        allowed_params = self.get_all_params()
        sorted_request_params = sorted([*self.data])
        sorted_allowed_params = sorted(allowed_params)
        invalid_params = [x for x in sorted_request_params if x not in sorted_allowed_params]
        if invalid_params:
            return False, {'error': 'invalid params found in request body. invalid parameters are {invalid_params}'
                .format(invalid_params=invalid_params)}
        return True,

    def get_validation_rule(self):
        """
        return validation rule specified in inherited class.
        :return: self.validation rule, a json.
        """
        return self.validation_rule

    def is_valid(self):
        """
        check if json data in request is valid or not.
        :param request: WSGI request
        :return: validation results
        """
        validation_response = self.validate_request_data()
        return validation_response

    def json_valid(self):
        """
        triggered if a json is validated successfully against a given rule.
        :return: json serialized object after saving it to database.
        """
        self.object = self.save()
        return JsonResponse(self.render_json(self.object, status_code=201))

    def json_invalid(self):
        """
        invoked if a json is not validated successfully against a given rule.
        :return: errors as json
        """
        return JsonResponse(self.error_dict, status=400)

    def post(self, request):
        """
        Override post method to make calls to self.is_valid()
        and go on with further proceedings.
        :param request: WSGI Request
        :return: Json serialized object if validation passes
        errors as json if validation fails.
        """
        if self.is_valid():
            print('valid_json')
            return self.json_valid()
        return self.json_invalid()

    def get_mandatory_param(self):
        """
        Return mandatory parameters in validation rule.
        :return: all mandatory params in validation rule
        if rule have mandatory params else None.
        """
        mandatory_params = [k for k, v in self.validation_rule.items()
                            if self.validation_rule.get(k).get('required') is not None]

        return mandatory_params if mandatory_params else None

    def get_all_params(self):
        """
        Returns all params given in a validation rule.
        :return: all params in a given validation rule
        """
        return [*self.validation_rule]

    def save(self, data=None):
        """
        Create an entry in database after successful validation.
        auto_populate_fields can be mentioned in inherited class.
        :param data: extra data if needed.
        :return: object corresponding to database entry.
        """
        data = data if data else self.data
        if hasattr(self, 'auto_populate_fields'):
            data.update({k: attrgetter(v)(self) for k, v in self.auto_populate_fields.items()})
        self.instance = self.model.objects.create(**data)
        return self.instance

    def render_json(self, obj, status_code):
        """
        returns json serialized objects
        :param obj: an object corresponding to a database entry.
        :return: json serialized objects.
        """

        return Response.get_formatted_response(Response(request=self.request, data=[obj]))

