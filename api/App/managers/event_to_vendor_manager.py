# Place to store querys and business logic
from django.db import models

class EventToVendorQueryset(models.query.QuerySet):
    def get_biz_event_by_id(self, id):
        return self.get(pk=id)

    def get_biz_event_by_id_and_vendor(self, vendor, event_id):
        return self.get(pk=event_id, vendor=vendor)

    def get_all_biz_vendor(self, user):
        return self.filter(vendor=user)

    def get_biz_event_by_vendor(self, vendor):
        return self.filter(vendor=vendor, analyst_assigned_vendor=True)
        

    def filter_biz_event_by_id(self, event_id):
        return self.filter(biz_event=event_id)
        

class EventToVendorManager(models.Manager):
    def get_queryset(self):
        return EventToVendorQueryset(self.model, using=self._db)

    def get_vendor_biz_events(self, user):
        """
        Given a vendor get all events the user is participating in
        """
        return self.get_queryset().get_all_biz_vendor(user)
        
    def get_biz_event_by_id(self, id):
        """
        Get all biz events 
        """
        return self.get_queryset().get_biz_event_by_id(id)
    def get_biz_event_by_vendor(self, vendor):
        """
        Get  biz event by vendor and event id
        """
        return self.get_queryset().get_biz_event_by_vendor(vendor)
    def filter_biz_event_by_id(self, event_id):
        """
        Filter vendor to biz events by event id
        """
        return self.get_queryset().filter_biz_event_by_id(event_id)

    def get_biz_event_by_id_and_vendor(self, vendor, event_id):
        """
        Filter vendor to biz events by event id
        """
        return self.get_queryset().get_biz_event_by_id_and_vendor(vendor, event_id)