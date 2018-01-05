

read_team = {
    'mandatory_params': {'name': str}
}

update_team = {
    'name': str,
    'description': str,
    'team_type': str, 'allowed_values': ['tech', 'management', 'business', 'marketing'],
    'members': list
}

delete_team = {
    'mandatory_params': {'name': str}
}

create_team = {
    'name': {'type': str, 'required': True},
    'description': {'type': str, 'required': True},
    'team_type': {'type': str, 'required': True, 'allowed_values': ['tech', 'management', 'business', 'marketing']},
    'members': {'type': list}
}