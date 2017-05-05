from django.http import JsonResponse
from django.views.generic import View

from permissions.decorators.decorator_switch import check_perms_fetch_object
from pyteam.mixins.validate_url_params import ValidateUrlParams
from response.response import Response


class RESTApi(ValidateUrlParams, View):
    @check_perms_fetch_object
    def get(self, request, **kwargs):
        """
        get object from kwargs as check_perms_fetch_object update kwargs with respective object
        if permission check passes.
        """
        if kwargs.get('response') is None:
            response = Response(request, kwargs.get('objects'))
            json_dump_params = response.get_json_dump_param()
            return JsonResponse(response.get_formatted_response(), json_dumps_params=json_dump_params, status=200)
        return kwargs.get('response')
