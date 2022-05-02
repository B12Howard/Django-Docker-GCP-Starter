from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
   path('login', views.LoginView.as_view(), name="login"),
   path('user', views.UserView.as_view(), name="user"),
]
