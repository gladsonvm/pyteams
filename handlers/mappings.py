from pyteaman.pyteams.models.Team import team_types
from django.contrib.auth.models import User
from datetime import datetime

mappings = {
    {
        'team':
            {
                 'create':  {
                     'name': str,
                     'description': str,
                     'created_by': User,
                     'team_type': [x[0] for x in team_types],
                     'created_on': str,
                     'updated_on': str
                 }

            }
    }
}