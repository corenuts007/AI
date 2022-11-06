from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from datetime import datetime
from spyproj import app

# If modifying these scopes, delete the file spyproj/token_gdrive.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
#SCOPES = ['https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable']
SCOPES = [
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.settings.basic',
]

class googleDriveUpload:

    def __init__(self):
        print("======>in __init__", os.path)
        print('in googleDriveUpload ****googleDriveUpload****************')

    def upload(self,video, imgName):
        try:
            #service = build('drive', 'v3', credentials=creds)
            print("google drive auth Started")
            #service=self.aut()
            print("google drive auth completed")
            currentDay = datetime.today().date()
            videoId= self.createRemoteFolder('videos')
             #createRemoteFolder
            parentID= self.createRemoteFolder(str(currentDay),videoId)
            #imgName += '.mp4'
            file_metadata = {'name': imgName, 
            'parents': [parentID]
            #,
            # 'type': 'anyone',
	         #                   'value': 'anyone',
	          #                  'role': 'reader'
            }
            #media = MediaFileUpload('C:/Users/server/Desktop/yoylo7/runs/detect/exp2/12_580.mp4',
            #mimetype='video/mp4')
            print("*************ggg====>",video)
            media = MediaFileUpload(video, mimetype='video/mp4')
            print("*************1111111====>",video)
            service=self.aut()
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
        # The file spyproj/token_gdrive.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        # Allow Gmail to read and write emails, and access settings like aliases.
        SCOPES = [
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.settings.basic',
        ]
        try:
            print('start in gDrive auth11')
            with app.app_context():
                #print(app.config["ENV"])
                print(app.config['credentials'])
                creds = app.config['credentials']
                service = build('drive', 'v3', credentials=creds)
                print("Gdrive AUTH COOOOOOOOOMpleted")
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
        return service

    def createRemoteFolder(self, folderName, parentID = None):
        print("======>in createRemoteFolder", os.path)
        service=self.aut()
        print("======>in create folder")
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