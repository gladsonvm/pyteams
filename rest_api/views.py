from django.views.generic import View
from django.http import HttpResponse
from api.decorators.decorator_switch import check_perms_fetch_object
from response_formatter.response import Response
from django.http import JsonResponse


class RESTApi(View):
    @check_perms_fetch_object
    def get(self, request, **kwargs):
        """
        get object from kwargs as check_perms_fetch_object update kwargs with respective object
        if permission check passes.
        """
        response = Response(request, [kwargs.get('obj')])
        return JsonResponse(response.get_formatted_response(), status=200)

