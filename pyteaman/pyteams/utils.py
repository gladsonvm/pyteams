from django.shortcuts import _get_queryset
from django.contrib.auth.models import User
from .models import UpdateTracker
from .models import Team
import datetime


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.
    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.
    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def update_tracker(model_instance, action=None):
    """
    Method to keep track of update to each and every model update
    :param model_instance: an object of any type
    :return: true if UpdateTracker instance created. else False
    """
    if type(model_instance).__name__ == 'Team':
        update_dict = {
            'model_name': 'team',
            'model_id': model_instance.id,
            'action': 'create' if action == 'create' else 'update',
            'updated_on': datetime.datetime.now(),
            'updated_by': model_instance.created_by
        }
        try:
            UpdateTracker.objects.create(**update_dict)
            return True
        except:
            return False


def validate_arguments(func_name, *args, **kwargs):
    """
    This method validates args/kwargs passed on to Teamhandler methods.
    :param func_name: name of any method defined in TeamHandler class
    :param args: arguments
    :param kwargs: optional/keyword arguments
    :return: True if validation test passes else False
    """
    if func_name == 'create_team':
        # validation for TeamHandler.create_team()
        team_types = Team.team_types
        mandatory_args = ['team_name', 'team_type', 'created_by', 'description']
        if len(args) == 4:
            if isinstance(args[0], str) and isinstance(args[1], str) and isinstance(args[2], User) and \
                    isinstance(args[3], str):
                if args[1] in [str(x[0]) for x in team_types]:
                    args_from = 'args'
                    return True, args_from
                return False
            return False
        elif bool(kwargs) and kwargs.keys() == mandatory_args:
            if isinstance(kwargs.get('created_by', None), User) and isinstance(kwargs.get('team_name',None), str) and \
                    isinstance(kwargs.get('team_type', None), str) and isinstance(kwargs.get('description', None), str):
                args_from = 'kwargs'
                return True, args_from
        return False
    if func_name == 'retrieve_team':
        # validation for TeamHandler.retrieve_team()
        mandatory_args = 'user'
        if len(args) == 1 or len(args) == 2:
            if isinstance(args[0], User):
                args_from = 'args'
                if len(args) == 2:
                    if isinstance(args[1], list):
                        return True, args_from
                    return False
                return True, args_from
            return False
        if bool(kwargs) and mandatory_args in kwargs.keys():
            if isinstance(kwargs.get('user', None), str):
                if 'members' in kwargs.keys():
                    if isinstance(kwargs.get('members', None), list):
                        return True
                    return False
                return True
        return False
