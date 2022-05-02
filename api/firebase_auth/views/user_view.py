# from ..serializers import BizEventSerializer, BizEventUpdateSerializer
from ..models import CustomUser
from django.apps import apps
from rest_framework import viewsets, permissions, status, filters, generics
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
# from django.contrib import auth
# from django.conf import settings
# from django.db import transaction, IntegrityError
from django.http import HttpResponse
# from rest_framework.permissions import IsAuthenticated

class UserView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get user properties
        """
        user = request.user 
        qs = CustomUser.objects.get(firebase_id=user)
        print('qs')
        print(qs.user_type)
        return Response(qs.user_type, status=status.HTTP_200_OK)