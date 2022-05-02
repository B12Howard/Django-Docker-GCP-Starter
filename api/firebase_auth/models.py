from django.db import models
from .custom_user_manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.apps import apps

#TODO assign users based on user_type to a group to control permissions
class CustomUser(AbstractBaseUser, PermissionsMixin):
    CLIENTADMIN = 'ClientAdmin'
    EVENTADMIN = 'EventAdmin'
    ANALYST = 'Analyst'
    VIEWER = 'Viewer'
    VENDOR = 'Vendor'
    groupENUM = (
        (CLIENTADMIN, 'ClientAdmin'),
        (EVENTADMIN, 'EventAdmin'),
        (ANALYST, 'Analyst'),
        (VIEWER, 'Viewer'),
        (VENDOR, 'Vendor'),
    )
    user_type = models.CharField(default='', max_length=100, choices=groupENUM)
    email = models.EmailField(_('email address'), unique=True)    
    is_staff = models.BooleanField(default=False)
    firebase_id = models.CharField(default='', max_length=40)
    user_type = models.CharField(default='', max_length=20)
    #TODO user_type translate this into group?
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.firebase_id)



