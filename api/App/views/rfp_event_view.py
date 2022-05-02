# Analysts create an biz event. Each biz event has an associated NDA and a bid template
# Analyst creates an biz event.
# Analyst selects vendors and then creates event
# Alert will be sent via email to the vendors

# Vendor opts in by signing NDA or clicking agree
# After agreeing a copy of the template will be made for the vendor
#

# Vendor should be able to see all their BIZ events

from ..serializers import BizEventSerializer, BizEventUpdateSerializer
from ..models import BidSheet, Category, VendorToBizEvent, BizEvent,CompanyProfile, Client
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
from ..services.google_drive import GoogleDriveServices

import datetime
# Use this apps.get_model("firebase_auth","CustomUser") to get the CustomUser model

class BizEventView(APIView):
    """
    Biz Event creation, editing

    Method
    ------
    get(self, request)
        Get by id or all
        return:
            Response with List of dictionaries
    post(self, request)
        Given a user and category create a Google Sheet of that category's template and assign it to the analyst
    """
    # permission_classes = (IsAuthenticated,)
    # TODO check if this Analystc is in the right Group

    def post(self, request):
        """
        Create a new BIZ Event
        args:
            request: 
            {String} templateUrl Google Sheet URL,
            {Datetime} startDate,
            {String} bizDescription,
            {String} bizName,
            {Datetime} endDate,
            {Number} clientId,

        """
        user = request.user 
        sheet_url = request.data.get('templateUrl')
        start_date = request.data.get('startDate')
        event_description = request.data.get('bizDescription')
        biz_event_name = request.data.get('bizName')
        end_date = request.data.get('endDate')
        client_id = request.data.get('client')
        
        now = datetime.datetime.utcnow()
        print(client_id)
        client = Client.objects.get(pk=client_id)
        # TODO create parent folder for this event
        # Get folder url
        # Get folder name label it name + date
        gs = GoogleDriveServices()
        # returns {'id': cloudFolder.id, 'folder_name':cloudFolder.name}
        folder = gs.create_folder(f'{biz_event_name} {client.name} {now}')
        print('folder')
        print(folder)
        # Create new BizEvent object
        data = {
            'event_description': event_description,
            'created_date': now,
            'start_date': start_date,
            'biz_event_name': biz_event_name,
            'template_url': sheet_url,
            'end_date': end_date,
            'creator': user.id,
            'client': client.id,
            'drive_folder_id': folder['id'],
            'drive_folder_name': folder['folder_name'],
            'date_edited': None
        }
        print(data)
        biz_event_serializer = BizEventSerializer(data=data)
        print(biz_event_serializer.is_valid())
        print('errors')
        print(biz_event_serializer.errors)
        if biz_event_serializer.is_valid(raise_exception=True):
            biz_event_serializer.save()
            return Response(biz_event_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response('Error Creating BIZ Event', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Get BIZ Event by id if given an id, all otherwise
        return:
            Response with List of dictionaries
        """
        user = request.user 
        event_id = request.query_params.get('id')
        
        # Get by id
        if event_id is not None:
            biz_event = BizEvent.objects.get_biz_event_by_id(event_id)
            payload = BizEventSerializer(biz_event).data
        # Get all
        else:
            biz_event = BizEvent.objects.get_all_biz_events()
            payload = []
            # TODO loop and turn into array
            # Turn the query set into an array of key value pairs
            for item in biz_event:                
                payload.append(
                BizEventSerializer(item).data
                )

        if payload is None:
            return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(payload, status=status.HTTP_200_OK)

    def put(self, request):
        """
        Update an BIZ Event (end_date, template_url, biz_event_name, start_date)
        args:
            request: 
            {Number} id BIZ Event id
            {String} templateUrl Google Sheet URL,
            {Datetime} startDate,
            {String} bizDescription,
            {String} bizName,
            {Datetime} endDate,
            {Number} clientId,
        """
        event_id = request.data.get('id')
        sheet_url = request.data.get('templateUrl')
        start_date = request.data.get('startDate')
        event_description = request.data.get('bizDescription')
        biz_event_name = request.data.get('bizName')
        end_date = request.data.get('endDate')
        client_id = request.data.get('clientId')
        
        now = datetime.datetime.utcnow()

        # Create new BizEvent object
        data = {
            'event_description': event_description,
            'start_date': start_date,
            'biz_event_name': biz_event_name,
            'template_url': sheet_url,
            'end_date': end_date,
            'date_edited': now,
            'client': client_id
        }

        biz_event_to_edit = BizEvent.objects.get_biz_event_by_id(event_id)
        # TODO do we need to check if is_active?

        if biz_event_to_edit is None:
            return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
        
        biz_event_serializer = BizEventUpdateSerializer(biz_event_to_edit, data=data, partial=True)
        if biz_event_serializer.is_valid(raise_exception=True):
            biz_event_serializer.save(data=data)
            return Response(biz_event_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Error Updated BIZ Event', status=status.HTTP_400_BAD_REQUEST)
