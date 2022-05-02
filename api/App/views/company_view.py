from ..serializers import CompanyProfileSerializer
from ..models import CompanyProfile
from django.apps import apps
from rest_framework import viewsets, permissions, status, filters, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib import auth
from django.conf import settings
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

import datetime
# Use this apps.get_model("firebase_auth","CustomUser") to get the CustomUser model

class CompanyView(APIView):
    """
    All things related to Company model

    Method
    ------
    get(self, request)
    """
    # permission_classes = (IsAuthenticated,)
    # TODO check if this Analystc is in the right Group

    def get(self, request):
        """
        
        """
        user = request.user 
        
        if user.user_type != 'Analyst':
            return Response('Error, unauthorized access', status=status.HTTP_400_BAD_REQUEST)

        companies = CompanyProfile.objects.all()
        payload = []
        # Turn the query set into an array of key value pairs
        for item in companies:                
            payload.append(
            CompanyProfileSerializer(item).data
            )

        if payload is None:
            return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(payload, status=status.HTTP_200_OK)
