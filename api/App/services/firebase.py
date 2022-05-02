import os
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from google.oauth2 import service_account

#TODO use os environ when runing Django server
SERVICE_ACCOUNT_FILE = './App/services/firebaseConfig.json'
cred = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE)

# default_app = firebase_admin.initialize_app(cred)

#TODO store creentials in .env and call via os
class FirebaseAdmin:
    def __init__(self):
        pass

    def get_user_by_email(self):
        """Check the email against the Firebase user's database for uniqueness
        
        Return: 
            Boolean. True if the email is not in the database, False if it already exists
        """
        try:
            existing_user = auth.get_user_by_email("howard.luong87@gmail.com")
            print(existing_user.uid)
            return True
        except Exception as error:
            print(error)
            return False        
    def check_email_unique(self, email):
        """Check the email against the Firebase user's database for uniqueness
        
        Return: 
            Boolean. True if the email is not in the database, False if it already exists
        """
        try:
            existing_user = auth.get_user_by_email(email)
            print(existing_user)
            return True
        except Exception as error:
            print(error)
            return False        

    def create_user(self, email, company_name, phone_number):
        """ Create user in Firebase
        Args: 
            {string} email
            {string} company_name
            {string} phone_number
        Returns: user object
        """
        import secrets
        import string
        
        try:
            alphabet = string.ascii_letters + string.digits
            temp_password = ''.join(secrets.choice(alphabet) for i in range(10))  # for a 10-character password
            user = auth.create_user(
                email=email,
                email_verified=False,
                phone_number=phone_number,
                password=temp_password,
                display_name=company_name,
                disabled=False
            )
            return user

        except Exception as error:
            print(error)
            return ''
            # return error message and send to someone/ log it

    def create_user_given_password(self, email, company_name, password):
        """ Create user in Firebase
        Args: 
            {string} email
            {string} company_name
            # {string} phone_number
        Returns: user object
        """
        # import secrets
        import string
        
        try:
            alphabet = string.ascii_letters + string.digits
            # temp_password = ''.join(secrets.choice(alphabet) for i in range(10))  # for a 10-character password
            user = auth.create_user(
                email=email,
                email_verified=False,
                # phone_number=phone_number,
                password=password,
                display_name=company_name,
                disabled=False
            )
            return user

        except Exception as error:
            print(error)
            return ''
            # return error message and send to someone/ log it


if __name__ == '__main__':
    uc = FirebaseAdmin()
    uc.get_user_by_email()