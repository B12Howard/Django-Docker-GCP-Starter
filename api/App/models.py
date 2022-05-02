from django.db import models
from django.utils import timezone
from django.apps import apps
from .managers import BizEventManager, EventToVendorManager
from django.conf import settings

# For Vendors
class CompanyProfile(models.Model):
    # remove user for a many to many model
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_company')
    company_name = models.CharField(default='', max_length=200)
    year_founded = models.CharField(default='', max_length=4)
    office_address = models.CharField(default='', max_length=200)
    plant_address = models.CharField(blank=True, null=True, default='', max_length=200)
    headquarters_address = models.CharField(default='', max_length=200)
    company_ownership = models.CharField(default='', max_length=50)
    number_of_employees = models.CharField(default='', max_length=4)
    annual_sales = models.DecimalField(default='', max_digits=21, decimal_places=2)
    supplier_type = models.CharField(default='', max_length=40)
    main_products_services = models.CharField(default='', max_length=1000)
    other_capabilities = models.CharField(default='', max_length=1000)
    company_website = models.CharField(default='', max_length=150)
    contact_person = models.CharField(default='', max_length=150)
    contact_person_position = models.CharField(default='', max_length=100)
    contact_person_phone = models.CharField(default='', max_length=15)
    contact_person_email = models.CharField(default='', max_length=100)
    description = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    qualitative_questionnaire_url = models.CharField(blank=True, null=True, max_length=150)



class Category(models.Model):
    DIRECT = 'Direct'
    INDIRECT = 'Indirect'
    groupENUM = (
        (DIRECT, 'Direct'),
        (INDIRECT, 'Indirect'),
    )
    level1 = models.CharField(blank=False, max_length=50, help_text="Direct vs Indirect")
    level2 = models.CharField(blank=False, max_length=50, help_text="Windstream, IT, Facilities, etc.")
    level3 = models.CharField(blank=False, max_length=50, help_text="Hardware, Office Supplies, Clerical, etc")
    level4 = models.CharField(blank=True, null=True, max_length=50)

class CompanyToCategory(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='company_category')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_company')

class AnalystProfile(models.Model):
    first_name = models.CharField(default='', max_length=100)
    last_name = models.CharField(default='', max_length=100)
    analyst_type = models.CharField(default='', max_length=20)
    # TODO associate analyst type to group


class BidSheet(models.Model):
    spreadsheet_url = models.CharField(blank=False, max_length=150, unique=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='bidsheet_category')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bidsheet_owner')
# https://stackoverflow.com/questions/43847173/cannot-import-models-from-another-app-in-django

# Client is the entity that is having a request for proposal
# TODO probably needs company information
class Client(models.Model):
    name =  models.CharField(max_length=150)
    company_website = models.CharField(default='', max_length=150)
    contact_person = models.CharField(default='', max_length=150)
    # contact_person_position = models.CharField(default='', max_length=100)
    contact_person_phone = models.CharField(default='', max_length=15)
    contact_person_email = models.CharField(default='', max_length=100)
    description = models.TextField(default='', null=True)

class UserToClient(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE, related_name='client_to_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_to_client')


class RoundToBizEvent(models.Model):
    round_name = models.CharField(blank=True, max_length=50)
    action_needed = models.CharField(blank=True, max_length=150)
    notes = models.CharField(blank=True, max_length=350)

class BizEvent(models.Model):
    event_description = models.CharField(blank=True, max_length=150)
    created_date = models.DateTimeField(default=timezone.now)
    start_date = models.DateTimeField()
    biz_event_name = models.CharField(blank=True, max_length=150)
    template_url = models.CharField(blank=True, max_length=200)
    end_date = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='biz_event_creator')
    date_edited =  models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    drive_folder_id = models.CharField(blank=True, max_length=150)
    drive_folder_name = models.CharField(blank=True, max_length=150)
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.CASCADE, related_name='client_to_biz_event')
    biz_round = models.ForeignKey(RoundToBizEvent, on_delete=models.CASCADE, related_name='vendor_to_biz_project')
    objects = BizEventManager()

class VendorToBizEvent(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor_to_biz_project')
    biz_event = models.ForeignKey(BizEvent, on_delete=models.CASCADE, related_name='biz_project_to_vendor')
    contract_id =  models.CharField(blank=True, null=True, max_length=150)
    contract_url = models.CharField(blank=True, null=True, max_length=200)
    nda_is_signed = models.BooleanField(default=False)
    date_signed = models.DateTimeField(blank=True, null=True)
    is_participating = models.BooleanField(default=False)
    analyst_assigned_vendor = models.BooleanField(default=False, help_text='True means the vendor can sign the nda, False means cannot proceed or vendor was taken off the list of participants')
    spreadsheet_id =  models.CharField(blank=True, null=True, max_length=150)
    spreadsheet_url = models.CharField(blank=True, null=True, max_length=150)
    
    objects = EventToVendorManager()


# Table to associate Clients to users
class ClientToUser(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_client')

class CompanyToUser(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='company_user')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_company')

# Table to associate an Event Admin to an Event 
class EventAdminToBizEvent(models.Model):
    event_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_admin_to_biz_event')
    biz_event = models.ForeignKey(BizEvent, on_delete=models.CASCADE, related_name='biz_project_to_event_admin')
    