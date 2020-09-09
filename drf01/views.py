from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response

class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        print("这是drf的get请求")
        return Response("DRF GET OK")

    def post(self, request, *args, **kwargs):
        print("这是drf的post请求")
        return Response("DRF POST OK")