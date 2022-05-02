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

class BidSheetView(APIView):
    """
    Handle fetching and creating Google sheets for a user

    Method
    ------
    post(self, request)
        Given a user and category create a Google Sheet of that category's template and assing it to the user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Create a copy of a template given the Category
        """
        # User 
        pass

    def get(self, request):
        """
        Get a User's Bid Sheets
        """
    def put(self, request):
        """
        Update end_date and other variables on BidSheet model
        """
    