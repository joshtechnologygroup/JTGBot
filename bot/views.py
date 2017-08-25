from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView


class BotApi(APIView):
    authentication_classes = []

    def get(self, *args, **kwargs):
        return Response({})
