from ..serializers import CompanyProfileSerializer, CustomuserSerializer
from ..models import BidSheet, Category, CompanyProfile
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
from ..services.firebase import FirebaseAdmin, auth
from django.core.mail import send_mail  
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags

import datetime

# Use this apps.get_model('firebase_auth","CustomUser')
class UserCreatorView(APIView):
    """
    User Creation view just for creating Vendors

    Method
    ------
    post(self, request)
        Create a user. In the request is a UserType which will determine the type of user created
    """

    def post(self, request):
        """
        Create a CustomUser
        """
        # Parse request
        email = request.payload.get('EmailAddress')
        company_name = request.payload.get('CompanyName')
        year_founded = request.payload.get('YearFounded')
        office_address = request.payload.get('OfficeAddress')
        headquarters = request.payload.get('HeadquartersAddress')
        plant_address = request.payload.get('Plant Address')
        company_ownership = request.payload.get('CompanyOwnership')
        number_employees = request.payload.get('NumberofEmployees')
        annual_sales = request.payload.get('AnnualSales)')
        supplier_type = request.payload.get('SupplierType')
        main_products = request.payload.get('MainProductsServicesOffered')
        other_capabilities = request.payload.get('OtherCapabilities')
        company_website = request.payload.get('CompanyWebsite')
        contact_person = request.payload.get('ContactPerson')
        position = request.payload.get('Position')
        phone_number = request.payload.get('PhoneNumberContactPerson')
        email_address = request.payload.get('EmailAddressContactPerson')
        user_type = request.payload.get('UserType')

        # Check if the email exists
        is_unique = FirebaseAdmin.check_email_unique(email)
        if is_unique is not True:
            return Response('Duplicate Email', status=status.HTTP_400_BAD_REQUEST)
 
        # Create a CustomUser if there is a non-duplicate email. Save to db        
        new_user = FirebaseAdmin.create_user(self, email, company_name, phone_number)

        user_serializer_data = {
            'email':email,
            'is_staff':False,
            'firebase_id':new_user.uid,
            'user_type': settings.AUTH_USER_MODEL.VENDOR,
        }
        user_serializer = CustomuserSerializer(data=user_serializer_data)
        #customer_email = request.data["2"]
        if user_serializer.is_valid(raise_exception=True):
            new_user = user_serializer.save()
        else:
            return Response('Error saving user', status=status.HTTP_403_FORBIDDEN)

        # Create CompanyProfile and associate it to CustomUser if UserType is Vendor

        company_serializer_data = {
            'user': new_user,
            'company_name': company_name,
            'year_founded': year_founded,
            'office_address': office_address,
            'plant_address': plant_address,
            'headquarters_address': headquarters,
            'company_ownership': company_ownership,
            'number_of_employees': number_employees,
            'annual_sales': annual_sales,
            'supplier_type': supplier_type,
            'main_products_services': main_products,
            'other_capabilities': other_capabilities,
            'company_website': company_website,
            'contact_person': contact_person,
            'contact_person_position': position,
            'contact_person_phone': phone_number,
            'contact_person_email': email_address,
            'description': '',
            'date_added': datetime.datetime.utcnow()
        }

        company_serializer = CompanyProfileSerializer(data=company_serializer_data)
        if company_serializer.is_valid(raise_exception=True):
            new_company = company_serializer.save()
        else:
            # TODO Send error to log
            return Response('Success', status=status.HTTP_403_FORBIDDEN)

        # Send email to user with link to their landing page with a temporary password
        action_code_settings = auth.ActionCodeSettings(
            url='https://www.example.com/checkout?cartId=1234',
            # handle_code_in_app=True,
            # ios_bundle_id='com.example.ios',
            # android_package_name='com.example.android',
            # android_install_app=True,
            # android_minimum_version='12',
            # dynamic_link_domain='coolapp.page.link',
        )

        link = auth.generate_password_reset_link(email, action_code_settings)
        

        # Construct password reset email from a template embedding the link, and send
        # using a custom SMTP server.
        context = ({"name": company_name, "reset_password_link": link})
        html_message = render_to_string('../emails/newuseremailtemplate.html', context)
        send_mail(
            # title:
            "Welecome to MyBIZ",
            # plain text message:
            strip_tags(html_message),
            # from:
            settings.EMAIL_HOST_ALIAS,
            # to:
            email,
            # html message:
            html_message=html_message
        )
        return Response('Success', status=status.HTTP_201_CREATED)