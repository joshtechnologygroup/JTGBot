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
        if request_client_secret_key in settings.BOT_SECRET_TOKEN:
            # The authenticate function returns a tuple (user, None) as we can not check whether the user exists
            # in the system, returns None in place of user
            return None, None
        else:
            # raise exception if Client secret key does not match
            raise exceptions.AuthenticationFailed('Incorrect Bot Key')
