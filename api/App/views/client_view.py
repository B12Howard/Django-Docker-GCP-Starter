from ..serializers import CustomuserSerializer, ClientSerializer, UserToClientSerializer
from ..models import Client
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
from ..services.firebase import FirebaseAdmin
import datetime
# Use this apps.get_model("firebase_auth","CustomUser") to get the CustomUser model

class ClientView(APIView):
    """
    All things related to Client model

    Method
    ------
    get(self, request)
    post(self, request)
    """
    # permission_classes = (IsAuthenticated,)
    # TODO check if this Analystc is in the right Group

    def get(self, request):
        """
        
        """
        user = request.user 
        
        if user.user_type != 'Analyst':
            return Response('Error, unauthorized access', status=status.HTTP_400_BAD_REQUEST)

        companies = Client.objects.all()
        payload = []
        # Turn the query set into an array of key value pairs
        for item in companies:                
            payload.append(
            ClientSerializer(item).data
            )

        if payload is None:
            return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(payload, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new Client
        args:
            request: 
            {String} companyName,
            {String} companyDescription,
            {String} contactPerson,
            {String} contactPersonPhone,
            {String} contactPersonEmail,
            {String} website,
            {String} password,

        """
        user = request.user 
        cn = request.data.get('companyName')
        cd = request.data.get('companyDescription')
        cp = request.data.get('contactPerson')
        cpp = request.data.get('contactPersonPhone')
        cpe = request.data.get('contactPersonEmail')
        ws = request.data.get('website')
        pword = request.data.get('password')
        
        now = datetime.datetime.utcnow()

        # Create new account in Firebase for this Client using the contactPersonEmail and password
        # If we get an error return error to user (most likely a duplicate email used)
        firebase_admin = FirebaseAdmin()
        unique_email = firebase_admin.check_email_unique
        if unique_email == False:
            Response('Error, email is already registered', status=status.HTTP_400_BAD_REQUEST)

        new_user = firebase_admin.create_user(cpe, cn, pword)

        # Save to table CustomUser with user_type Client with new firebase.uid
        user_serializer_data = {
                'email': cpe,
                'is_staff': False,
                'firebase_id': new_user.uid,
                'user_type': settings.AUTH_USER_MODEL.CLIENTADMIN,
            }
        user_serializer = CustomuserSerializer(data=user_serializer_data)
        
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
        else:
            return Response('Error saving user', status=status.HTTP_403_FORBIDDEN)

        data = {
            'name': cn,
            'description': cd,
            'company_website': ws,
            'contact_person': cp,
            'contact_person_phone': cpp,
            'contact_person_email': cpe,           
        }
        # TODO add atomic here
        # Then after saving the new user create a new Client associating client to the new user in the UserToClient table
        client_serializer = ClientSerializer(data=data)
        if client_serializer.is_valid(raise_exception=True):
            new_client = client_serializer.save()
            
            # Associate new Client and new User in UserToClient table
            data = {
                'client': new_client,
                'user': new_user
            }
            
            utc_serializer = UserToClientSerializer(data=data)
            if utc_serializer.is_valid(raise_exception=True):
                utc_serializer.save()

            # TODO Return the new user email and the company it is associated with                
            return Response(client_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Error Creating BIZ Event', status=status.HTTP_400_BAD_REQUEST)
