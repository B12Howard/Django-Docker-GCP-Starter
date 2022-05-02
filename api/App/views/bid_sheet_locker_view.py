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

class BidSheetLockerView(APIView):
    """
    For task scheduler to call and look for  any bidsheets that are at or past due date, then lock is to that only people of the domain mmg can view/edit it
    https://stackoverflow.com/questions/38434401/google-sheets-api-setting-permissions

    Method
    ------
    post(self, request)
        Scan bidsheet table for at or past due date
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Scan bidsheet table for at or past due date. Lock the spreadsheet from public view if at or past due date.
        """
        pass