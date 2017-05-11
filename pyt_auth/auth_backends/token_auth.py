from django.contrib.auth import get_user_model
from pyt_auth.models import AuthToken
from pyt_auth.exceptions.exceptions import TokenDoesNotExist


class TokenAuthentication(object):

    def authenticate(self, request, token):
        try:
            user = AuthToken.objects.get(pk=token).user
            return user
        except:
            raise TokenDoesNotExist
