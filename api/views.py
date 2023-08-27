from django.shortcuts import render
from rest_framework.views import APIView
from .utils import generate_successful_response
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class SecretView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return generate_successful_response("Yoooo")