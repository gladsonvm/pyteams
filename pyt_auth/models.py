import binascii
import os
from django.db import models
from django.contrib.auth.models import User


class AuthToken(models.Model):
    token = models.CharField(max_length=40, primary_key=True)
    user = models.OneToOneField(User)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(AuthToken, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token

