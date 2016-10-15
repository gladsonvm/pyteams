from django.shortcuts import _get_queryset
from django.contrib.auth.models import User


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

def build_response(**kwargs):
    status = {
        0: 'failed',
        1: 'success',
        2: 'created',
        3: 'not created'

    }
    import ipdb;ipdb.set_trace();


def get_user_on_user_identifier(user_identifier):
    if len(user_identifier.strip(' ')):
        user = get_object_or_None(User, username=user_identifier)
        if user is None:
            user = get_object_or_None(User, email=user_identifier)
        if user:
            return user
    return None
