# Create your views here.
import json

from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView

from bot import utils as bot_utils
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
            if api_response['status']['code'] == 200:
                if not api_response['result']['actionIncomplete']:
                    intent_name = api_response['result']['metadata']['intentName']
                    if intent_name == 'Contact_Request_Get_By_Name':
                        response = bot_utils.get_contact_info_by_name(
                            api_response['result']['parameters']['JTG_Employee'],
                            email,
                            api_response['result']['fulfillment']['speech']
                        )
                    elif intent_name == 'Vacation_Query_Available':
                        parameters = api_response['result']['parameters']
                        response = bot_utils.get_official_leaves(
                            parameters['Vacation_Type_Available'],
                            parameters['date-period'],
                        )
                    elif intent_name == 'Vacation_Query_Remaining':
                        parameters = api_response['result']['parameters']
                        identity = parameters['JTG_Employee'] or data['email']
                        vaction_type = parameters['Vacation_Type_Remaining']
                        response = bot_utils.get_remaining_leaves_for_user(identity, vaction_type)
                    elif intent_name == 'Vacation_Query_Team_Status':
                        parameters = api_response['result']['parameters']
                        response = bot_utils.get_team_status(parameters['JTG_Team'], parameters['date'])
                    elif intent_name == 'Vacation_Apply':
                        parameters = api_response['result']['parameters']
                        response = bot_utils.apply_vaction(data['email'], parameters['Date_Entity'], parameters['Vacation_Type_Apply'])
                    else:
                        response = {}
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
        if settings.MM_TOKEN == data['token']:
            email = json.loads(settings.MM_CONFIG).get(data['user_name'])
            kwargs.update({'email': email, 'query': data.get('text', '')})
            response = super(MMBotVerificationApi, self).post(*args, **kwargs)
            response = Response({"text": response.data})
        return response or Response({}, status=401)
