# Create your views here.
import json

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from bot import (
    constants as bot_constants,
    utils as bot_utils,
)
from bot.authentications import BoTAuthentication


class BotApi(APIView):
    authentication_classes = [BoTAuthentication]

    def post(self, *args, **kwargs):
        data = self.request.data
        query = data.get('query') or kwargs.get('query')
        email = data.get('email') or kwargs.get('email')
        if email and query:
            api_response = bot_utils.call_bot_api(query, email)
            response = 'Time to learn something new'
            if api_response['status']['code'] in range(200, 220):
                if not api_response['result']['actionIncomplete']:
                    intent_name = api_response['result']['metadata'].get('intentName', '')
                    kwargs = {
                        'parameters': api_response['result']['parameters'],
                        'email': email,
                        'query': query,
                        'response_text': api_response['result']['fulfillment']['speech'],
                        'api_response': api_response
                    }
                    response = bot_constants.INTENT_RESPONSE_MAPPING.get(intent_name,bot_constants.INTENT_RESPONSE_MAPPING['default'])(**kwargs)
                else:
                    response = api_response['result']['fulfillment']['speech']
        else:
            return Response({}, 400)
        return Response(response)


class MMBotVerificationApi(BotApi):
    authentication_classes = []

    def post(self, *args, **kwargs):
        data = self.request.data
        response = None
        if data.get('token') == settings.MM_TOKEN:
            email = json.loads(settings.MM_CONFIG).get(data['user_name'])
            kwargs.update({'email': email, 'query': data.get('text', '')})
            response = super(MMBotVerificationApi, self).post(*args, **kwargs)
            response = Response({"text": response.data})
        return response or Response({}, status=401)
