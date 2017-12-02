from django.contrib.auth import get_user_model
from pyt_auth.models import AuthToken
from pyt_auth.exceptions.exceptions import TokenDoesNotExist
from django.contrib.auth.models import User


class TokenAuthentication(object):

    def authenticate(self, token):
        try:
            user = AuthToken.objects.get(pk=token).user
            return user
        except:
            raise TokenDoesNotExist

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
