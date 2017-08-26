# Create your views here.
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from bot import utils as bot_utils


class BotApi(APIView):
    authentication_classes = []

    def post(self, *args, **kwargs):
        data = self.request.data
        api_response = bot_utils.call_bot_api(data.get('query'), data['email'])
        if not api_response['result']['actionIncomplete']:
            intent_name = api_response['result']['metadata']['intentName']
            if intent_name == 'Contact_Request_Get_By_Name':
                response = bot_utils.get_contact_info_by_name(api_response['result']['parameters']['JTG_Employee'])
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
            else:
                response = {}
        else:
            response = api_response['result']['fulfillment']['speech']
        return Response(response)


class SlackBotVerificationApi(BotApi):
    authentication_classes = []

    def post(self, *args, **kwargs):
        token = self.request.data.get('token')
        response = None
        if token == settings.SLACK_TOKEN:
            challenge = self.request.data.get('challenge', '')
            if challenge:
                response = Response(challenge)
            else:
                response = super(SlackBotVerificationApi, self).post(*args, **kwargs)
        return response or Response({}, status=401)
