from django.conf import settings
from rest_framework import (
    authentication,
    exceptions
)


class BoTAuthentication(authentication.BaseAuthentication):
    """
    Custom Authentication based on the client secret key in the request headers
    """
    def authenticate(self, request):
        # Get the client secret key from the request
        request_client_secret_key = request.META.get('HTTP_BOT_SECRET_TOKEN')
        # Authorize if the key is in known keys.
        if request_client_secret_key == settings.BOT_SECRET_TOKEN:
            return None, None
        else:
            # raise exception if Client bot key does not match
            raise exceptions.AuthenticationFailed('Incorrect Bot Key')
