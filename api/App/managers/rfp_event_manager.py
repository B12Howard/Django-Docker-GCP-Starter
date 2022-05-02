# Place to store querys and business logic
from django.db import models

class BizEventQueryset(models.query.QuerySet):
    def get_biz_event_by_id(self, event_id):
        return self.get(pk=event_id, )
    def get_all_biz_events(self):
        return self.all()
        

class BizEventManager(models.Manager):
    def get_queryset(self):
        return BizEventQueryset(self.model, using=self._db)

    def get_biz_event_by_id(self, id):
        """
        Given an id query the biz event
        """
        return self.get_queryset().get_biz_event_by_id(id)
        
    def get_all_biz_events(self):
        """
        Get all biz events 
        """
        return self.get_queryset().get_all_biz_events()