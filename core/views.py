from django.shortcuts import render
from django.views.generic import View, CreateView
from django.http.response import JsonResponse
from core.models import Team
from core.validators.request_data_validator import RequestDataValidatorMixin
from django.db

class TeamView(RequestDataValidatorMixin, View):
    model = Team
    # 1. get request data
    # 2. validate request data
    # 3. create entry in database
    # 4. return formatted response
    def get(self):

        return JsonResponse({'msg': 'OK'})

    def post(self, request, *args , **kwargs):
        self.data.update({'created_by': request.user})
        try:
            team = Team.objects.create(**self.data)
        except IntegrityError:

        return JsonResponse({'status': 'ok'}, status=200)


