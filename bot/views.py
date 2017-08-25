import json
import apiai

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class BotApi(APIView):
    authentication_classes = []

    def post(self, *args, **kwargs):
        CLIENT_ACCESS_TOKEN = 'ac3f28e051014b94b5666b89482f3d5c'
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        data = self.request.data
        request = ai.text_request()
        request.lang = 'en'
        request.session_id = 'ada6c87f-3048-43e1-8b9d-86dbe6abb90f'
        request.query = data.get('query', '')
        response = request.getresponse()
        response = json.loads(response.read())
        print response, type(response)
        if not response['result']['actionIncomplete']:
            # Intent_name = response['result']['metadata']['intentName']
            # data = process[Intent_name](a['result'])
            # Response(data)
            pass
        return Response(response['result']['fulfillment']['speech'])
