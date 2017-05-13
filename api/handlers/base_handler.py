import inspect
from django.db.utils import IntegrityError
from guardian.shortcuts import assign_perm
from api.mappings.handler_mappings import handler_model_mappings
from api.mappings.permissions.raw_permissions import raw_perm_mappings



class BaseHandler(object):
    """
    Base class which implements CRUD operations for handlers. This is a layer of abstraction over django model manager
    which allows to create objects for the corresponding code with minimal code. A handler should implement from
    BaseHandler and pass model to __init__() of BaseHandler. Private methods are used to make sure methods are accessed
    through entry point only and note that adding an '_' before a var/method doesnt make it really private, also
    adding a '__' mangles python namespace besides, "we are all consenting adults here".
    https://mail.python.org/pipermail/tutor/2003-October/025932.html
    """
    def __init__(self, handle):
        self.handle = handle
        self.model = handler_model_mappings.get(self.handle)
        self.available_methods = inspect.getmembers(self, predicate=inspect.ismethod)

    def create(self, param_dict):
        """
        Create a new model object with values specified in param_dict
        :param param_dict: dict with keys/values to create an object
        :return: object
        """
        _response = dict()
        try:
            obj = self.model.objects.create(**param_dict)
            perm_string = raw_perm_mappings.get(self.handle).get('get')
            assign_perm(perm_string, param_dict.get('created_by'), obj) 
        except IntegrityError:
            _response.update({'success': False, 'error': 'object already exists', 'status_code': 409})
        else:
            _response.update({'success': True, 'data': [obj], 'status_code': 201})
        finally:
            return _response

    def update(self, identifiers, param_dict):
        """
        update an existing object with values in param_dict.
        :param identifiers: key value pair to get object
        :param param_dict: key value pairs corresponding to fields to be updated
        :return: updated object
        """
        return self.model.objects.get(**identifiers).update(**param_dict)

    def delete(self, identifiers):
        """
        delete an existing object
        :param identifiers: key value pairs to get object
        :return: None
        """
        self.model.objects.get(**identifiers).delete()
        return None

    def execute(self, method, identifires=None, param_dict=None):
        """
        execute() acts as entry point to all methods in BaseHandler other than init. execute() run method as per
        name specified by method parameter if validation passes.
        :param method: string corresponds to name of a method other than __init__ and execute of BaseHandler.
        :return: results obtained after executing method of BaseHandler.
        """
        _method_map = dict()
        [_method_map.update({x[0]:x[1]}) for x in self.available_methods]
        return _method_map.get(method)(param_dict)

