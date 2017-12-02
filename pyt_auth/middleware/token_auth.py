from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate
from django.http import JsonResponse
from pyt_auth.exceptions.exceptions import (TokenDoesNotExist, TokenExpired, MalformedHeader)


class TokenAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            try:
                auth_token = self.extract_auth_token(auth_header)
                user = authenticate(request=request, token=auth_token)
                request.user = user
            except TokenDoesNotExist:
                return JsonResponse({'error': 'Token does not exist'}, status=404)
            except TokenExpired:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except MalformedHeader:
                return JsonResponse({'error': 'Malformed HTTP HEADER'}, status=400)
        elif not request.user.is_authenticated:
            return JsonResponse({'error': 'No auth token found in header'}, status=400)
        return None

    def extract_auth_token(self, auth_header):
        try:
            token = auth_header.split(' ')[1]
            param_name = auth_header.split(' ')[0]
            if isinstance(token, str) and param_name == 'Token' and len(token) == 40:
                return token
        except:
            raise MalformedHeader
