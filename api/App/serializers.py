from django.conf import settings
from rest_framework import serializers
from .models import CompanyProfile, VendorToBizEvent, BizEvent, Client, UserToClient, CompanyToUser
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.apps import apps

class CustomuserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = (
            'email',
            'is_staff',
            'firebase_id',
            'user_type',
        )

class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = (
            'id',
            'company_name',
            'year_founded',
            'office_address',
            'plant_address',
            'headquarters_address',
            'company_ownership',
            'number_of_employees',
            'annual_sales',
            'supplier_type',
            'main_products_services',
            'other_capabilities',
            'company_website',
            'contact_person',
            'contact_person_position',
            'contact_person_phone',
            'contact_person_email',
            'description',
            'date_added',
        )

class ClientSerializer(serializers.ModelSerializer):
    # vendor = serializers.StringRelatedField(many=False)

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'company_website',
            'contact_person',
            'contact_person_phone',
            'contact_person_email',
            'description',
        )

class UserToClientSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = UserToClient
        fields = (
            'client',
            'user',
        )

class UserToVendorCompany(serializers.ModelSerializer):
    company = serializers.StringRelatedField(many=False)
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = CompanyToUser
        fields = (
            'company',
            'user',
        )

class BizEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizEvent
        fields = (
            'event_description',
            'created_date',
            'start_date',
            'biz_event_name',
            'template_url',
            'end_date',
            'creator',
            'date_edited',
            'client',
            'drive_folder_id',
            'drive_folder_name'
        )

class ForVendorBizEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizEvent
        fields = (
            'event_description',
            'created_date',
            'start_date',
            'biz_event_name',
            'end_date',
        )

class BizEventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizEvent
        fields = (
            'event_description',
            'start_date',
            'biz_event_name',
            'template_url',
            'end_date',
            'date_edited',
            'client'
        )

class VendorToBizEventSerializer(serializers.ModelSerializer):
   class Meta:
        model = VendorToBizEvent
        fields = ( 
            'vendor',
            'biz_event',
            'contract_id',
            'contract_url',
            'nda_is_signed',
            'date_signed',
            'is_participating',
            'analyst_assigned_vendor',
            'spreadsheet_id',
            'spreadsheet_url'
            )

class SignedNDAVendorToBizEventSerializer(serializers.ModelSerializer):
   class Meta:
        model = VendorToBizEvent
        fields = ( 
            'id',
            'biz_event',
            'contract_id',
            'contract_url',
            'nda_is_signed',
            'date_signed',
            'is_participating',
            'analyst_assigned_vendor',
            'spreadsheet_id',
            'spreadsheet_url'
            )

class ForVendorVendorToBizEventSerializer(serializers.ModelSerializer):
   class Meta:
        model = VendorToBizEvent
        fields = ( 
            'id',
            'biz_event',
            'contract_id',
            'contract_url',
            'nda_is_signed',
            'date_signed',
            'is_participating',
            'analyst_assigned_vendor',
            )

class VendorToBizEventNDASerializer(serializers.ModelSerializer):
   class Meta:
        model = VendorToBizEvent
        fields = ( 
            'nda_is_signed'
            )