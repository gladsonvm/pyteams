import json
from django.http import JsonResponse
from django.views.generic import View
from pyteam.mixins.validate_url_params import ValidateRequestParams
from api.handlers.base_handler import BaseHandler
from api.mappings.handler_mappings import handler_method_mappings
from response.response import Response


class TeamApi(ValidateRequestParams, View):

    def get(self, request, **kwargs):
        """
        get object from kwargs as check_perms_fetch_object update kwargs with respective object
        if permission check passes.
        """
        response = Response(request, {'success': True, 'data': kwargs.get('objects')})
        json_dump_params = response.get_json_dump_param()
        return JsonResponse(response.get_formatted_response(), json_dumps_params=json_dump_params, status=200)

    def post(self, request, *args, **kwargs):
        """
        perform create operations after checking permissions.
        """
        post_dict = json.loads(request.body.decode('utf-8'))
        post_dict.update({'created_by': request.user})
        handler = BaseHandler(kwargs.get('handle'))
        handler_response = handler.execute(method='create', param_dict=post_dict)
        status_code = handler_response.get('status_code')
        response = Response(request, handler_response)
        json_dump_params = response.get_json_dump_param()
        return JsonResponse(response.get_formatted_response(), json_dumps_params=json_dump_params, status=status_code)

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
