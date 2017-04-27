from pyteam.validators import mappings as validator_mappings


class Validator(object):
    """
    Class that wraps up all the methods necessary for validating arguments passed to TeamHandler.
    """

    def get_validator_dict(self):
        return validator_mappings.get(self)

    def create_validator(self, **kwargs):
        validator_dict = validator_mappings.get('TeamValidator').get('create')
        validated = False
        for key, value in validator_dict.items():
            for param, param_value in kwargs.items():
                if key == param:
                    if type(value) is list:
                        if param_value in value:
                            validated = True
                        else:
                            validated = False
                    elif type(param_value) is value:
                        validated = True
                    else:
                        validated = False
        if not validated:
            raise Exception('Validation error.')
