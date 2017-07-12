

def get_object_or_none(model, lookup_param, lookup_value):
    lookup_kwargs = {lookup_param: lookup_value}
    try:
        return model.objects.get(**lookup_kwargs)
    except model.DoesNotExist:
        return None
