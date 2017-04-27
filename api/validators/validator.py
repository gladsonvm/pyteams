from api.mappings import validator_mappings


class Validator(object):
    """
    Class that wraps up all the methods necessary for validating arguments passed to TeamHandler.
    """

    def __init__(self, handler, method, param_dict):
        """
        This method validates parameters passed to a handler based on action.
        :param handler: name of handler
        :param method: method name
        :param param_dict: named args passed to method
        :return: True if validates else raise exception.
        """
        validator_dict = validator_mappings.get(handler).get(method)
        validated = False
        for key, value in validator_dict.items():
            for param, param_value in param_dict.items():
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
            raise Exception('Validation Failed.')
        return True
