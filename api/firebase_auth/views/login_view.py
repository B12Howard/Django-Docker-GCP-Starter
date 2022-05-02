from django.shortcuts import render

# from rest_framework.authentication import SessionAuthentication, FirebaseAuthentication
from ..authentication import FirebaseAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class LoginView(APIView):
    authentication_classes = [FirebaseAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)