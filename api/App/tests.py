from django.test import TestCase
from .models import *
import datetime
import json
from unittest.mock import MagicMock
from unittest.mock import patch
from rest_framework.test import APIRequestFactory

class BidSheetTest(TestCase):
    def test_google_drive_api_access_vendor_folder(self):
        pass
    def test_create_bid_sheet_from_template(self):
        pass

class UserTest(TestCase):
    def test_create_profile_for_a_vendor_user_type(self):
        pass

# 3/31 1800 tested TODO created automated tests
class BizEventTest(TestCase):
    def test_create_biz_event(self):
        # return list of >2 dict
        pass    
    def test_get_biz_event_by_id(self):
        # return list of one dict
        pass    
    def test_get_biz_event_by_id_none_matching(self):
        # return blank list
        pass    
    def test_get_all_biz_event(self):
        pass    
    def test_update_biz_event_by_id(self):
        # assume test data has no word edit in the description and null edited date
        # test if name has edited in it
        # test if there is an edited date
        pass    

class BizEventParticipantViewTest(TestCase):
    def test_add_vendor(self):
        pass
    def test_get_biz_event_participants_by_id_as_analyst(self):
        pass
    def test_get_biz_event_participants_all_as_analyst(self):
        pass
    def test_get_biz_event_participants_all_as_vendor(self):
        pass
    def test_add_vendors_to_event_should_set_assigned_vendor_false(self):
        # Test data
        #         {
        #     "vendorIdsKv": {"4":True},
        #     "eventId":1
        # }
        # for vendor_id in vendor_ids:
        #     # Check if the vendor is already attached to this event
        #     exists = VendorToBizEvent.objects.get_biz_event_by_vendor(vendor_id, event_id).exists()
        #     # For vendor value True
        #     if vendor_ids[vendor_id] == True:
        #         print("true")
        #         print(exists)
        #         # IF vendor is attached to this event do nothing
        #         if exists == True:
        #             print("do nothing true")
        #         # If vendor is not attached to this event add vendor to event and set analyst_assigned_vendor True
        #         else:
        #             print("add to db")
        #             print("set analyst_assigned_vendor true")
        #     # For vendor value False
        #     elif vendor_ids[vendor_id] == False:
        #         print("false")
        #         print(exists)
        #         # IF vendor is attached to this event set analyst_assigned_vendor False
        #         if exists == True:
        #             print("set analyst_assigned_vendor false")
        #         # If vendor is not attached to this event do nothing
        #         else:
        #             print("do nothing true")        
        pass
    def test_add_vendors_to_event_should_set_assigned_vendor_true(self):
        pass
    def test_vendor_gets_own_vendorevents_returns_events(self):
        pass
    def test_analyst_vendorevents_by_id(self):
        pass

class SignNDA(TestCase):
    def test_sign_nda(self):
        pass
    def test_user_has_no_matching_id(self):
        pass
    def test_user_has_matching_id(self):
        pass
    def test_sign_true(self):
        pass
    def test_sign_false(self):
        pass
