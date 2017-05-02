from django.contrib.auth.decorators import permission_required as django_perm_req
from api.decorators.guardian_perm_req import permission_required as guardian_perm_req
from pyteam.models import Team

permission_decorator_mappings = {
    'handles': {
        'team': {
            'actions':  {
                'get': guardian_perm_req('pyteam.retrieve_team', (Team, 'id', 'id')),
                'create': django_perm_req('pyteams.add_team', raise_exception=True),
                'update': guardian_perm_req('pyteam.change_team', (Team, 'id', 'id')),
                'delete': guardian_perm_req('pyteam.delete_team', (Team, 'id', 'id'))
                }
            }
        }
    }


