from django.shortcuts import _get_queryset
from django.contrib.auth.models import User
from .models import UpdateTracker
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


def get_user_on_user_identifier(user_identifier):
    if len(user_identifier.strip(' ')):
        user = get_object_or_None(User, username=user_identifier)
        if user is None:
            user = get_object_or_None(User, email=user_identifier)
        if user:
            return user
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



