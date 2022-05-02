from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    path('biz-event', views.BizEventView.as_view(), name="biz-event"),
    path('biz-event-participant', views.BizEventParticipantView.as_view(), name="biz-event-participant"),
    path('single-biz-event-participant', views.SingleBizEventParticipantView.as_view(), name="single-biz-event-participant"),
    path('my-nda', views.NDAView.as_view(), name="nda"),
    path('company', views.CompanyView.as_view(), name="company"),
    path('client', views.ClientView.as_view(), name="client"),
]
