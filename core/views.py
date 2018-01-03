from django.shortcuts import render
from django.views.generic import View, CreateView
from django.http.response import JsonResponse
from core.models import Team
import json
from core.forms import TeamCreateForm
from core.validators.request_data_validator import RequestDataValidatorMixin, RDVMixin, JSONResponseMixin, JSONFormView
from core.validators.rules import create_team
from django.db import IntegrityError
from django.views.generic.base import TemplateResponseMixin
from django.http import JsonResponse
from sierra.dj.mixins.forms import JSONFormMixin
from django.views.generic.edit import ModelFormMixin
from mixins.auto_populate_form_kwargs import AutoPopulateFormKwargs
from operator import attrgetter


class TeamCreateView(RequestDataValidatorMixin, View):
    model = Team
    auto_populate_fields = {'created_by': 'request.user', 'last_updated_by': 'request.user'}
    validation_rule = create_team

    # def get_form_kwargs(self):
    #     """
    #     Returns the keyword arguments for instantiating the form.
    #     """
    #     data = json.loads(self.request.body.decode('UTF-8'))
    #     # import ipdb;ipdb.set_trace()
    #     if hasattr(self, 'auto_populate_fields'):
    #         data.update({k: attrgetter(v)(self) for k, v in self.auto_populate_fields.items()})
    #     kwargs = super(ModelFormMixin, self).get_form_kwargs()
    #     kwargs.update({'data': data})
    #     if hasattr(self, 'object'):
    #         kwargs.update({'instance': self.object})
    #     print('\n---data', kwargs, '-----\n')
    #     return kwargs

    # # 1. get request data
    # # 2. validate request data
    # # 3. create entry in database
    # # 4. return formatted response
    # def get(self):
    #
    #     return JsonResponse({'msg': 'OK'})
    #
    # def post(self, request, *args , **kwargs):
    #
    #     # self.data.update({'created_by': request.user})
    #     data = json.loads(request.body.decode('UTF-8'))
    #     team = Team.objects.create(**data)
    #     # except IntegrityError:
    #     #     return JsonResponse({'status': 'already exists'}, status=409)
    #     return JsonResponse({'status': 'ok'}, status=200)


