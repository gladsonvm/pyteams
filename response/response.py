import datetime


class Response(object):
    """
    This class returns json formatted response after serializing given object to json format.
    call get_formatted_response by passing data as a list of objects, eg [obj,]
    Request meta data will be added to response json.
    """
    def __init__(self, request, data):
        self.request = request
        self.data = data
        if not isinstance(data, list):
            raise Exception('data must be a list of objects.')

    def get_formatted_response(self):
        """
        This method iterates over a list of objects, converts each one to json serialized entries
        and append the same to object_list. meta info for a request is also added to response
        upon calling this method
        :return: dict with object list ad=nd meta info
        """
        object_list = list()
        response = dict()
        if len(self.data):
            # append only if objects exists.
            for obj in self.data:
                object_list.append(self.clean_object(obj))
        response['meta'] = {
            'resource_uri': self.request.get_full_path(),
            'total_objects': len(object_list),
        }
        response['objects'] = object_list
        return response

    def clean_object(self, obj):
        """
        This method returns given object as a dict after converting datetime to string
        and removing unnecessary params from dict
        :param object: object
        :return: dict without key _state
        """

        serialized_object = obj.__dict__
        for key in serialized_object:
            serialized_object[key] = str(serialized_object[key])
            if isinstance(serialized_object[key], datetime.datetime):
                serialized_object[key] = serialized_object[key].isoformat()
        if '_state' in serialized_object:
            # remove django model state entry from serialized dict
            del [serialized_object['_state']]
        return serialized_object

    def get_json_dump_param(self):
        json_dump_params = {'indent': 2} if self.request.GET.get('pretty') is not None else dict()
        return json_dump_params