import json
from core.validators.rules import get_validation_rule, get_all_params
from django.http import JsonResponse
from django.views.generic.edit import ModelFormMixin
from django.views.generic.edit import BaseFormView
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import FormMixin
from operator import attrgetter
from response.response import Response

class RequestDataValidatorMixin(object):
    """
    This class bounds all methods necessary to validate request data and provide a formatted output
    """

    def _validate_request_data(self, request):
        """
        This method is the entry point for provide formatted data after successful validation.
        :param request: WSGI request.
        :return: None if validation passes if any one validation fails, then appropriate error msg.
        """
        validators = [self._validate_request_body, self._validate_mandatory_params, self._validate_allowed_params]
        if hasattr(self, 'validators'):
            if type(self.validators) is list:
                validators = validators + self.validators
            else:
                raise TypeError('Validators provided in %s must be a list', self.__class__.__name__)

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
        mandatory_params = self.get_mandatory_param()
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

    def _validate_allowed_params(self, request):
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

    def post(self, request, *args, **kwargs):
        validation_response = self._validate_request_data(request)
        if validation_response[0] is False:
            return JsonResponse(validation_response[1], status=400)
        self.object = self.save()
        return self.render_json()

    def get_mandatory_param(self):
        if self.validation_rule.get('mandatory_params'):
            return [[*param][0] for param in self.validation_rule.get('mandatory_params')]
        return None

    def get_all_params(self):
            return [x for x in [*self.validation_rule] if x != 'mandatory_params'] + self.get_mandatory_param()

    def save(self, data=None):
        data = data if data else self.data
        if hasattr(self, 'auto_populate_fields'):
            data.update({k: attrgetter(v)(self) for k, v in self.auto_populate_fields.items()})
        self.instance = self.model.objects.create(**data)
        return self.instance

    def render_json(self):
        return JsonResponse(Response.get_formatted_response(Response(request=self.request, data=[self.object])))


class RDVMixin(object):
    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        self.data = json.loads(self.request.body.decode('UTF-8'))
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs
    # def get_form_kwargs(self):
    #     """
    #     Returns the keyword arguments for instantiating the form.
    #     """
    #     kwargs = {
    #         'initial': self.get_initial(),
    #         'prefix': self.get_prefix(),
    #     }
    #
    #     if self.request.method in ('POST', 'PUT'):
    #         kwargs.update({
    #             'data': json.loads(self.request.body.decode('UTF-8')),
    #             'files': self.request.FILES,
    #         })
    #         self.data = kwargs.get('data')
    #     return kwargs

    # def render_to_response(self, context, **response_kwargs):
    #     """
    #     Returns a response, using the `response_class` for this
    #     view, with a template rendered with the given context.
    #     If any keyword arguments are provided, they will be
    #     passed to the constructor of the response class.
    #     """
    #     response_kwargs.setdefault('content_type', self.content_type)
    #     return self.response_class(
    #         data=self.data
    #     )
    # def get_context_data(self, **kwargs):
    #     """
    #     Insert the single object into the context dict.
    #     """
    #     context = {}
    #     if self.object:
    #         context['object'] = self.object
    #         context_object_name = self.get_context_object_name(self.object)
    #         if context_object_name:
    #             context[context_object_name] = self.object
    #     context.update(kwargs)
    #     return super(SingleObjectMixin, self).get_context_data(**context)

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            context,
            **response_kwargs
        )

    def get_context_data(self, **kwargs):
        """
        Insert the form into the context dict.
        """
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        return super(FormMixin, self).get_context_data(**kwargs)




class JSONFormView(JSONResponseMixin, BaseFormView):
    """
    An attempt to integrate a JSONView with a FormView.
    Basically, the idea is this- JSON views will not require a GET method.
    Since POST is the only concern, we need to pass the post data into
    the form, then respond with JSON data instead of Form data.
    Several Overrides are the attempt to manipulate the BaseFormView to
    respond with JSON data, rather than starting from scratch.
    """

    def get_form_class(self):
        """
        There will be issues if form_class is None, so override this
        method to check and see if we have one or not.
        """
        form_class = super(JSONFormView, self).get_form_class()
        if form_class is None:
            raise ImproperlyConfigured(
                "No form class to validate. Please set form_class on"
                " the view or override 'get_form_class()'.")
        return form_class

    def get_success_url(self):
        """
        Overridden to ensure that JSON data gets returned, rather
        than HttpResponseRedirect, which is bad.
        """
        return None

    def form_valid(self, form):
        """
        Overridden to ensure that an HttpResponseRedirect does not get
        called with a success_url -- instead render_to_response some
        JSON data. DO NOT CALL SUPER!
        @note: We return a JSON flag - { success: true }. Because this
        is a common paradigm in Ben programming. However, it seems that
        the flag should be { valid: true }. Discuss amongst yourselves.
        """
        self.object = form.save()
        return self.render_to_response(self.get_context_data(success=True))

    def form_invalid(self, form):
        """
        Overridden to ensure that a form object isn't returned, since
        that has some weird serialization issues. Instead pass back
        the errors from the form, and a JSON flag - { success: false }.
        @note: See form_valid for more discussion on the JSON flag.
        """
        # context = self.get_context_data(success=False)
        context = form.errors
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        """
        Overridden so that on a GET request the response isn't allowed.
        JSON Forms are intrinsinctly POST driven things, a GET makes
        no sense in the context of a form. (What would you get?). For
        Normal HTTP, you would pass back an empty form, but that's
        pretty usesless for JSON. So we pwn this entire method right
        off the bat to ensure no screwiness or excessive net traffic.
        """
        return HttpResponseNotAllowed(['GET', ])
