import inspect

from pyteam.mappings.handler_mappings import handler_model_mappings
from pyteam.validators.validator import Validator


class BaseHandler(object):
    """
    Base class which implements CRUD operations for handlers. This is a layer of abstraction over django model manager
    which allows to create objects for the corresponding code with minimal code. A handler should implement from
    BaseHandler and pass model to __init__() of BaseHandler.
    """
    # todo: implement permission decorators for every methods
    def __init__(self, handle):
        self.handle = handle
        self.model = handler_model_mappings.get(self.handle)

    def create(self, param_dict):
        Validator.validate(inspect.currentframe().f_code.co_name, param_dict)
        return self.model.objects.create(**param_dict)

    def update(self, model_id, param_dict):
        Validator.validate(inspect.currentframe().f_code.co_name, param_dict)
        return self.model.objects.get(param_dict.get(model_id)).update(**param_dict)

    def delete(self, model_id):
        self.model.objects.get(model_id).delete()
        return self.handle + ':' + model_id
