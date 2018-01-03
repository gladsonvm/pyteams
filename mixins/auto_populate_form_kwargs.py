import json
from django.views.generic.edit import ModelFormMixin


class AutoPopulateFormKwargs(object):
    def get_form_kwargs(self):
        """
        overriding django's default get_form_kwargs to populate fields which must be updated with data in request.
        """
        data = json.loads(self.request.body.decode('UTF-8'))
        data.update({'created_by': self.request.user})
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'data': data})
        if hasattr(self, 'auto_populate_fields'):
            import ipdb;ipdb.set_trace()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs