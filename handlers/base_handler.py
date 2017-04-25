from validators.validator import Validator
import inspect


class BaseHandler(Validator):
    """
    Base class which implements CRUD operations for handlers. This is a layer of abstraction over django model manager
    which allows to create objects for the corresponding code with minimal code. A handler should implement from
    BaseHandler and pass model to __init__() of BaseHandler.
    """
    def __init__(self, handle):
        self.handle = handle
        super(Validator, self).__init__()

    def create(self, handler, param_dict):
        # Validator.validate(handler=handler, method=inspect.currentframe().f_code.co_name, param_dict=param_dict)
        return self.model.objects.create(**param_dict)

    # def update(self):
