from django.http import JsonResponse
from django.views.generic import View
from pyteam.mixins.validate_url_params import ValidateUrlParams
from api.handlers.base_handler import BaseHandler
from api.mappings.handler_mappings import handler_method_mappings
from response.response import Response


class RESTApi(ValidateUrlParams, View):

    def get(self, request, **kwargs):
        """
        get object from kwargs as check_perms_fetch_object update kwargs with respective object
        if permission check passes.
        """
        print('\n view kwargs-->', kwargs)
        if kwargs.get('response') is None:
            response = Response(request, kwargs.get('objects'))
            json_dump_params = response.get_json_dump_param()
            return JsonResponse(response.get_formatted_response(), json_dumps_params=json_dump_params, status=200)
        return kwargs.get('response')

    def post(self, request, *args, **kwargs):
        """
        perform create operations after checking permissions.
        """
        handler = BaseHandler(kwargs.get('handle'))

        pass

    def patch(self, request, *args, **kwargs):
        """
        perform partial update to object referred by URI
        """
        pass

    def put(self):
        """
        perform full update/replace object referred by URI
        """
        pass


class ApiInfo(View):
    """
    Returns info for different api endpoints.
    """
    # todo: make ApiInfo generalized using mappings and mixins.
    def get(self, request):
        endpoint = request.GET.get('endpoint')
        info_type = request.GET.get('type')
        if endpoint == '/handler/method/' and info_type == 'permissions':
            return JsonResponse(handler_method_mappings, status=200)
        return JsonResponse({'error': 'Bad request'}, status=400)
