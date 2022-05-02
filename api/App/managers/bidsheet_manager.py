# Place to store querys and business logic
from django.db import models

class BidSheetQueryset(models.query.QuerySet):
    def bidsheet_by_category_query(self, category):
        pass

class BidSheetManager(models.Manager):
    def get_bidsheet_by_category(self):
        pass

    def get_bidsheets_by_user(self):
        """
        Given a user type use different querys.
        Analysts will get all bid sheets
        Vendors will only get their sheets
        """
        pass
    def get_bidsheets_by_user_and_category(self):
        """
        Given a user type use different querys.
        Analysts will get all bid sheets for a Category
        Vendors will only get their sheets for a Category
        """
        pass