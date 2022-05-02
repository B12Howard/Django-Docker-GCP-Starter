from ..serializers import VendorToBizEventSerializer, SignedNDAVendorToBizEventSerializer, ForVendorVendorToBizEventSerializer, BizEventSerializer, ForVendorBizEventSerializer
from ..models import BidSheet, Category, VendorToBizEvent, BizEvent
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
from django.db import transaction, IntegrityError

# Use this apps.get_model("firebase_auth","CustomUser") to get the CustomUser model
# Analysts create an biz event. Each biz event has an associated NDA and a bid template
# Analyst creates an biz event.
# Analyst selects vendors and then creates event
# Alert will be sent via email to the vendors

# Vendor opts in by signing NDA or clicking agree
# After agreeing a copy of the template will be made for the vendor

# Vendor should be able to see all their BIZ events
class SingleBizEventParticipantView(APIView):
    """
    Handle get and edits of one signel biz participant event

    Method
    ------
    get(self, request)
        return:
    put(self, request)
    """
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """

            return: 
                Response with List of dictionaries
        """
        user = request.user 
        print(user.id)
        print(user.user_type)
        event_id = request.query_params.get('eventId')
        payload = []

        # For case of user type is Analyst
        # if user.user_type == 'Analyst':
        #     if event_id is not None:
        #         biz_events = VendorToBizEvent.objects.filter_biz_event_by_id(event_id)
        #         for item in biz_events:
        #             payload.append(
        #                 VendorToBizEventSerializer(item).data
        #             )    
                # payload = [VendorToBizEventSerializer(biz_event).data]
            # else:
            #     # User type is Vendor get all or user type Analyst and no id was provided
            #     # Get all for Vendor
            #     biz_events = VendorToBizEvent.objects.get_vendor_biz_events(user)
            #     # Turn the query set into an array of key value pairs
            #     for item in biz_events:
            #         payload.append(
            #             VendorToBizEventSerializer(item).data
            #         )    

        # For case of user type is Vendor
        if user.user_type == 'Vendor':
            print("VENDOR")
            #Get all of this vendor's bizevents
            biz_event = VendorToBizEvent.objects.get_biz_event_by_id_and_vendor(user.id, event_id)
            
            # biz_events = VendorToBizEvent.objects.get_vendor_biz_events(user)
            # Turn the query set into an array of key value pairs
            if biz_event is None:
                return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
            # Check if siogned NDA
            if biz_event.nda_is_signed:
            # IF signed use SignedNDAVendorToBizEventSerializer
                payload = {**SignedNDAVendorToBizEventSerializer(biz_event).data, **ForVendorBizEventSerializer(biz_event.biz_event).data}
            # Else ForVendorVendorToBizEventSerializer
            else:
                payload = {**ForVendorVendorToBizEventSerializer(biz_event).data, **ForVendorBizEventSerializer(biz_event.biz_event).data}


        if payload is None:
            return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(payload, status=status.HTTP_200_OK)
