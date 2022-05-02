#from ..serializers import
from ..models import BidSheet, Category
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

# Use this apps.get_model("firebase_auth","CustomUser") to get the CustomUser model

class Vendor(APIView):
    permission_classes = (IsAuthenticated,)
    """
    Vendor related views

    Method
    ------
    post(self, reqest)
        
    """