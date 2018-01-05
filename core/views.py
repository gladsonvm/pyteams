from django.views.generic import View
from core.models import Team
from core.validators.request_data_validator import RequestDataValidatorMixin
from core.validators.rules import create_team, create_team


class TeamCreateView(RequestDataValidatorMixin):
    model = Team
    auto_populate_fields = {'created_by': 'request.user', 'last_updated_by': 'request.user'}
    exclude_fields = []
    validation_rule = create_team

