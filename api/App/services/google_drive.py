from apiclient import discovery
import googleapiclient.discovery
import sys
from apiclient import errors

#TODO store creentials in .env and call via os
class GoogleDriveServices:
    def __init__(self):
        pass

    def credentials_from_file(self):
        """Load credentials from a service account file
        Args:
            None
        Returns: service account credential object
        
        https://developers.google.com/identity/protocols/OAuth2ServiceAccount
        """
        
        from google.oauth2 import service_account
        import googleapiclient.discovery

        # https://developers.google.com/identity/protocols/googlescopes#drivev3
        SCOPES = [
            'https://www.googleapis.com/auth/drive'
        ]
        # SERVICE_ACCOUNT_FILE = './name-of-service-account-key.json'
        SERVICE_ACCOUNT_FILE = './App/services/firebaseConfig.json'
        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
                
        return credentials

    def create_bid_sheet(self, template, folder, vendor):
        """
        Create bid sheet from template
        args:
            string template id of the sheet template
            string folder id of this specific biz event's folder
            string vendor vendor's name
        return:
            dict {id, sheet_name}
        """
        origin_file_id = template
        title = vendor
        parent = folder
        credentials = self.credentials_from_file()
        copied_file = {
            "title": title,
            "parents": [parent]
        }
       
        service = discovery.build("drive", "v3", credentials=credentials)
        try:
            file = service.files().copy(
                fileId=origin_file_id, body=copied_file).execute()
            
            # print(file)
            return {"id": file.id, "sheet_name": file.name}
        except errors.HttpError:
            print (f"An error occurred: {errors.HttpError}")
            return {"id": "", "sheet_name": ""}
    
    def create_folder(self, biz_event_name):
        """
        When an biz event is created create a folder to store any future event to vendor spreadsheet
        Put it into the main folder of id 1Rlei5mccoHGE53VLjk-iN2WfeRLAXOAh so that anyone can get accesss to the spreadsheets given a link
        args:
            string biz_event_name
        return:
            dict {id, folder_name}
        """
        name = biz_event_name if biz_event_name is not None else "Placeholder Biz Event"
        credentials = self.credentials_from_file()
        folder_metadata = {
        'name': name,
        'parents': ["1Rlei5mccoHGE53VLjk-iN2WfeRLAXOAh"],
        'mimeType': 'application/vnd.google-apps.folder'
        }
        service = discovery.build('drive', 'v3', credentials=credentials)
        cloudFolder = service.files().create(body=folder_metadata, supportsAllDrives=True).execute()
        print('cloudFolder')
        print(cloudFolder)
        return {'id': cloudFolder['id'], 'folder_name':cloudFolder['name']}
    
    def move_file_to_folder(self, file, folder):
        """
        Given a file id move it to the folder of given id
        """
        pass
    def get_all_templates(self):
        """
        Get all template spreadsheet urls and titles from the Template Folder in the Google Drive
        """
        pass

    def lock_spreadsheet(self, spreadsheet):
        """
        Given a spreadsheet id set permissions so that only app people can acceess it
        """
if __name__ == '__main__':
    uc = GoogleDriveServices()
    print(sys.argv[1])
    print(sys.argv[2])
    print(sys.argv[3])
    uc.create_bid_sheet(sys.argv[1], sys.argv[2], sys.argv[3])