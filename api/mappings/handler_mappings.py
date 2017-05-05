from django.contrib.auth.models import User
from pyteam.models import Team

mappings = {
    'team':
        {
             'create':  {
                 'name': str,
                 'description': str,
                 'created_by': User,
                 'team_type': [x[0] for x in Team.team_types],
                 'created_on': str,
                 'updated_on': str
             }

        }
    }


handler_model_mappings = {
    'team': Team
}

handler_method_mappings = {
    'team': ['get', 'create', 'update', 'delete'],
    'task': ['get', 'create', 'update', 'delete'],
}
