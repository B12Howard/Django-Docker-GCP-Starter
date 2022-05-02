from ..serializers import ForVendorBizEventSerializer, SignedNDAVendorToBizEventSerializer, VendorToBizEventSerializer, ForVendorVendorToBizEventSerializer
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
import datetime

class NDAView(APIView):
    def put(self, request):
        """
        Update an nda's signed status
        request:
            vendorEventId
            signedBool
        """
        user = request.user
        signed_bool = request.data.get('signedBool')
        vendor_event_id =  request.data.get('vendorEventId')
        print(signed_bool)
        print(vendor_event_id)
        # Given an event_id look for all the matching VendorToBizEvents biz_event
        #  for false filter with "in" for matches update existing ones
        # for true filter with not in if possible then create 
        if vendor_event_id == None or signed_bool == None:
            return Response('No blank answers allowed', status=status.HTTP_400_BAD_REQUEST)

        qs = VendorToBizEvent.objects.get_biz_event_by_id_and_vendor(user.id, vendor_event_id)
        print(qs.nda_is_signed)
        if qs:
            print('found one')
            if qs.nda_is_signed == False:
                print('signing')
                data = {
                    'nda_is_signed': True,
                    'date_signed': datetime.datetime.utcnow(),
                    'is_participating': True
                }
                
                serializer = VendorToBizEventSerializer(qs, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
        else:
            print("No matching biz event for this vendor")
            return Response('No matching biz event for this vendor', status=status.HTTP_204_NO_CONTENT)
        
        payload =  { **SignedNDAVendorToBizEventSerializer(qs).data, **ForVendorBizEventSerializer(qs.biz_event).data }
        # Return the vendor biz event with a spreadsheet url
        return Response(payload, status=status.HTTP_200_OK)