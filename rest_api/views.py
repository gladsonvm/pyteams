from django.views.generic import View
from django.http import HttpResponse
from api.decorators.decorator_switch import check_perms_fetch_object


class RESTApi(View):
    @check_perms_fetch_object
    def get(self, request, **kwargs):
        print(kwargs)
        return HttpResponse('Test View')

