from core.models import Team

# todo: make rules dynamic based on models instead of creating rule of each model

create_team = {
    'mandatory_params': [
        {'name': str},
        {'description': str},
        {'team_type': str, 'allowed_values': [team_type[0] for team_type in Team.team_types]}
    ],
    'members': list
}

read_team = {
    'mandatory_params': {'name': str}
}

update_team = {
    'name': str,
    'description': str,
    'team_type': str, 'allowed_values': [team_type[0] for team_type in Team.team_types],
    'members': list
}

delete_team = {
    'mandatory_params': {'name': str}
}


def get_mandatory_param(rule):
    if rule.get('mandatory_params'):
        return [[*param][0] for param in rule.get('mandatory_params')]
    return None


def get_validation_rule(instance, request_method):
    if type(instance).__name__ == 'TeamView' and request_method.lower() == 'post':
        return create_team


def get_all_params(instance, request_method):
    if type(instance).__name__ == 'TeamView' and request_method.lower() == 'post':
        return [x for x in [*create_team] if x != 'mandatory_params'] + get_mandatory_param(create_team)
