from ..serializers import VendorToBizEventSerializer, ForVendorVendorToBizEventSerializer, BizEventSerializer, ForVendorBizEventSerializer
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
from ..services.google_drive import GoogleDriveServices

# Use this apps.get_model("firebase_auth","CustomUser") to get the CustomUser model
# Analysts create an biz event. Each biz event has an associated NDA and a bid template
# Analyst creates an biz event.
# Analyst selects vendors and then creates event
# Alert will be sent via email to the vendors

# Vendor opts in by signing NDA or clicking agree
# After agreeing a copy of the template will be made for the vendor

# Vendor should be able to see all their BIZ events
class BizEventParticipantView(APIView):
    """
    Manage BIZ Events for Vendors. Edit vendors participation to a project

    Method
    ------
    get(self, request)
        Get a given BIZ Event or All if no id is given
        return:
            Response with List of dictionaries
    put(self, request)
        Edit a vendors participation to an BIZ Event
    """
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Get BIZ Events participants by event id, else get all biz events created by analyst
        If the user is an AnalystGet BIZ Event by id if given an id, all BIZ Events otherwise
        If the user is a Vendor get all BIZ Events that the vendor belongs to
            return: 
                Response with List of dictionaries
        """
        user = request.user 
        print(user.id)
        print(user.user_type)
        event_id = request.query_params.get('id')
        payload = []

        # For case of user type is Analyst
        if user.user_type == 'Analyst':
            if event_id is not None:
                biz_events = VendorToBizEvent.objects.filter_biz_event_by_id(event_id)
                for item in biz_events:
                    payload.append(
                        VendorToBizEventSerializer(item).data
                    )    
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
            biz_events = VendorToBizEvent.objects.get_biz_event_by_vendor(user.id)
            # biz_events = VendorToBizEvent.objects.get_vendor_biz_events(user)
            # Turn the query set into an array of key value pairs
            for item in biz_events:
                payload.append(
                {
                    **ForVendorVendorToBizEventSerializer(item).data, **ForVendorBizEventSerializer(item.biz_event).data
                    # 'event_to_vedor':ForVendorVendorToBizEventSerializer(item).data,
                    # 'event_info': ForVendorBizEventSerializer(item.biz_event).data
                }    
                )

        if payload is None:
            return Response('Error, no matching BIZ Event', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(payload, status=status.HTTP_200_OK)

    #TODO Generate a contract id and contract url
    def put(self, request):
        """
        Update a vendor to biz event relationship
        request:
            vendorIdsKv key value pair of vendorIds: boolean as to whether to add or remove the Vendor from the VendorToBizEvent table
            eventId id of the biz event
        """
        vendor_ids = request.data.get('vendorIdsKv')
        event_id =  request.data.get('eventId')

        # Given an event_id look for all the matching VendorToBizEvents biz_event
        #  for false filter with "in" for matches update existing ones
        # for true filter with not in if possible then create 
        if event_id == None or vendor_ids == None:
            return Response('No event id or vendors given', status=status.HTTP_400_BAD_REQUEST)
    
        for vendor_id in vendor_ids:
            # Check if the vendor is already attached to this event
            biz_event_qs = VendorToBizEvent.objects.get_biz_event_by_vendor(vendor_id, event_id)
            exists = biz_event_qs.exists()
            # For vendor value True
            if vendor_ids[vendor_id] == True:
                print("true")
                print(exists)
                # IF vendor is attached to this event do nothing
                if exists == True:
                    print("set analyst_assigned_vendor true")
                    data = {
                        'analyst_assigned_vendor': True 
                    }
                    # event = BizEvent.objects.get_biz_event_by_id(event_id)
                    serializer = VendorToBizEventSerializer(biz_event_qs[0], data=data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                # If vendor is not attached to this event add vendor to event and set analyst_assigned_vendor True
                else:
                    print("add to db")
                    print("set analyst_assigned_vendor true")
                    # TODO create a copy of the spreadsheet template
                    gd = GoogleDriveServices()
                    # gd.create_bid_sheet(sys.argv[1], sys.argv[2], sys.argv[3])

                    data = {
                        'vendor': vendor_id, 
                        'biz_event': event_id, 
                        'contract_id': None, 
                        'contract_url': None, 
                        'nda_is_signed': False, 
                        'date_signed': None, 
                        'is_participating': False, 
                        'analyst_assigned_vendor': True 
                    }

                    serializer = VendorToBizEventSerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        
            # For vendor value False
            elif vendor_ids[vendor_id] == False:
                print("false")
                print(exists)
                # IF vendor is attached to this event set analyst_assigned_vendor False
                if exists == True:
                    print("set analyst_assigned_vendor false")
                    data = {
                        'analyst_assigned_vendor': False 
                    }
                    # event = BizEvent.objects.get_biz_event_by_id(event_id)
                    serializer = VendorToBizEventSerializer(biz_event_qs[0], data=data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        
                # If vendor is not attached to this event do nothing
                else:
                    print("do nothing F")

            print("=======")
        print(event_id)
        return Response('Success', status=status.HTTP_200_OK)
        # data = {'link': link, 'date_submitted': now }
        # serializer_submission = serializers.SubmissionSerializer(latest_submission, data=data, partial=True)

        # if serializer_submission.is_valid(raise_exception=True):
        #     serializer_submission.save(data=data)
        #     res = Response_Dto('success', 'Your link has been updated', {})
        #     return Response(res.json_res(), status=status.HTTP_200_OK)

        # try:
        #     with transaction.atomic(): 
        #         # In this row of data get the link
        #         # Get the data from the submission table by matching by link
        #         for link_id in row:
        #             submission = Submission_queryset.get(pk=link_id)
                    
        #             # Loop through list of assignees for this link
        #             for commenter_email in row[link_id]:
        #                 # Get the user object based on email
        #                 assignee = User_queryset.get(email__iexact=commenter_email)
        #                 #submission = Submission_queryset.get(link__iexact=link)
        #                 serializer = AssignmentSerializer(data={'assignee':assignee, 'submission':submission.id, 'is_complete':False})
        #                 if serializer.is_valid(raise_exception=True):
        #                     serializer.save(assignee=assignee, submission=submission, is_complete=False)
        #                 else: 
        #                     raise IntegrityError

        #             # Update is_assigned to true for this submission
        #             data = {"is_assigned": True, "date_assigned": datetime.datetime.utcnow()}
        #             serializer_submission = SubmissionSerializer(submission, data=data, partial=True)
        #             if serializer_submission.is_valid():
        #                 serializer_submission.save()
        #             else: 
        #                 raise IntegrityError

        # except IntegrityError:
        #     # Email to admin
        #     # subject = 'Error Updating Assignment'
        #     # message = 'The Pod ID ' + pod_id
        #     # email_from = settings.EMAIL_HOST_ALIAS
        #     # recipient_list = [settings.CUSTOM_EMAIL_FOR_ERRORS]
        #     # send_mail( subject, message, email_from, recipient_list)
        #     return Response('Error Assigning Vendors to BIZ Event', status=status.HTTP_400_BAD_REQUEST)
