from django.contrib.auth.decorators import permission_required as django_perm_req
from permissions.decorators.guardian_perm_req import permission_required as guardian_perm_req
from pyteam.models import (Team, Task, Activity)

permission_decorator_mappings = {
    'handles': {
        'team': {
            'actions':  {
                'get': guardian_perm_req('pyteam.retrieve_team', (Team, 'id', 'id')),
                'create': django_perm_req('pyteams.add_team', raise_exception=True),
                'update': guardian_perm_req('pyteam.change_team', (Team, 'id', 'id')),
                'delete': guardian_perm_req('pyteam.delete_team', (Team, 'id', 'id'))
                }
            },
        'task': {
            'actions': {
                'get': guardian_perm_req('pyteam.retrieve_task', (Task, 'id', 'id')),
                'create': django_perm_req('pyteams.add_task', raise_exception=True),
                'update': guardian_perm_req('pyteam.change_task', (Task, 'id', 'id')),
                'delete': guardian_perm_req('pyteam.delete_task', (Task, 'id', 'id'))
            }
        },
        'activity': {
            'actions': {
                'get': guardian_perm_req('pyteam.retrieve_activity', (Activity, 'id', 'id')),
                'create': django_perm_req('pyteams.add_activity', raise_exception=True),
                'update': guardian_perm_req('pyteam.change_activity', (Activity, 'id', 'id')),
                'delete': guardian_perm_req('pyteam.delete_activity', (Activity, 'id', 'id'))
            }
        }
    }
}



