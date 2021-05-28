from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token

class MyAuth(authentication.BaseAuthentication):

    def authenticate(self, request):

        key_string = request.META.get('HTTP_SECRET')

        if not key_string:
             return None

        obj = Token.objects.select_related('user').get(key=key_string)

        if not (obj.user and obj.user.is_active):
            raise exceptions.AuthenticationFailed('User does not exist')

        return (obj.user, key_string)
