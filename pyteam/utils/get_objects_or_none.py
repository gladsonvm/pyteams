

def get_objects_or_none(model, request, lookup_value):
    is_filter_query = False
    lookup_field = request.GET.get('lookup_field')
    if not lookup_value:
        is_filter_query = True
        # this should be obtained from a mapping dict as different model may have different query fields
        lookup_field = 'created_by'
        lookup_value = request.user
    elif lookup_field is None and lookup_value.isdigit():
        lookup_field = 'id'
    elif lookup_field is None and lookup_value.isalpha():
        lookup_field = 'name'
    lookup_kwargs = {lookup_field: lookup_value}

    try:
        if is_filter_query:
            return model.objects.filter(**lookup_kwargs)
        return [model.objects.get(**lookup_kwargs)]
    except model.DoesNotExist:
        return None
