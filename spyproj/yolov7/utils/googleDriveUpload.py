from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import datetime

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
#SCOPES = ['https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable']
SCOPES = ['https://www.googleapis.com/auth/drive']

class googleDriveUpload:

    def __init__(self):
        print('hi')

    def upload(self,video, imgName):
        try:
            #service = build('drive', 'v3', credentials=creds)
            service=self.aut();
            currentDay = datetime.today().date()
             #createRemoteFolder
            parentID= self.createRemoteFolder(str(currentDay))
            imgName += '.mp4'
            file_metadata = {'name': imgName, 
            'parents': [parentID],
             'type': 'anyone',
	                            'value': 'anyone',
	                            'role': 'reader'
            }
            #media = MediaFileUpload('C:/Users/server/Desktop/yoylo7/runs/detect/exp2/12_580.mp4',
            #mimetype='video/mp4')
            print("*************ggg====>",video)
            media = MediaFileUpload(video, mimetype='video/mp4')
            print("*************1111111====>",video)
            file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id,webViewLink').execute()
            print ('File Linkkk---',file.get('webViewLink'))    

            return file.get('webViewLink')
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
    def aut(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        print("========>",os.path)
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            #print("nooooo 1t if")
            if creds and creds.expired and creds.refresh_token:
                #print("nooooo 2nddd if")
                creds.refresh(Request())
            else:
                #print("else else else")
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials1.json', SCOPES)
                #print("else 1111111111111111")
                flow.redirect_uri = 'http://localhost:5001/'

                creds = flow.run_local_server(port=5001)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
        return service

    def createRemoteFolder(self, folderName, parentID = None):
        service=self.aut()
        folderlist=service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          ).execute()
        #print("======>",str(folderlist))
        titlelist = folderlist.get('files', [])
        #print('**********',str(titlelist))
        for item in titlelist:
            print("*******",item['name'])
            print("*******--",folderName)
            if item['name']==folderName:
                return item['id']
        file_metadata = {
            'name': folderName,
            'mimeType': 'application/vnd.google-apps.folder',
        }
        
        file = service.files().create(body=file_metadata,
                                    fields='id').execute()
        return file['id']