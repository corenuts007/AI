from __future__ import print_function

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime
import flask
from spyproj import app
import requests
from flask import Flask, redirect, request, render_template
import os
import ffmpeg 
#from ffmpeg_streaming import Formats
import io
import shutil, sys  
from spyproj.utils.simplegmail.gmail import Gmail
from spyproj.repository.cameradetails_repository import CameraDetails
from spyproj.repository.alertdetails_repository import AlertDetails
from spyproj.repository.cameradetails_repository import CameraDetails
from spyproj.model.camera_details_data import CameraDetailsData
import subprocess
import time





# If modifying these scopes, delete the file spyproj/token_gdrive.json.
#SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
#SCOPES = ['https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable']
SCOPES = [
        
         'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.appdata',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.metadata',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.settings.basic'
]

class googleDriveUpload:

    def __init__(self):
        #print("======>in __init__", os.path)
        print('googleDriveUpload')

    def upload(self,video, imgName):
        try:
            service=self.aut()
            #service = build('drive', 'v3', credentials=creds)
            currentDay = datetime.today().date()
            print('upload 111111111',video)
            print('upload 111111111',imgName)
            videoId= self.createRemoteFolder('convertedVideos', service,None)
            print('upload 22222')
             #createRemoteFolder
            parentID= self.createRemoteFolder(str(currentDay), service, videoId)
            print('upload 3333')
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
            #print("*************1111111====>",video)
            file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id,webViewLink').execute()
            print ('***Upload END     *******      File Linkkk---',file.get('webViewLink'))    

            return file.get('webViewLink')
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
    
    
    def move(self,file_id,destFolder):
        try:
            service=self.aut()
            #service = build('drive', 'v3', credentials=creds)
            currentDay = datetime.today().date()
            d4 = currentDay.strftime("%d-%b-%Y")
            #print('destFolder move 1111', destFolder)
            destFolderId= self.createRemoteFolder(destFolder, service,None)
            #print(' parentFolderId move 22222', destFolderId)
             #createRemoteFolder
            parentID= self.createRemoteFolder(str(d4), service, destFolderId)
            #print('****************************************************************')
            #print('parentID upload 3333', parentID)

            file = service.files().get(fileId=file_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            #print('previous_parents upload 3333', previous_parents)
            #print('****************************************************************')

                # Move the file to the new folder
            file = service.files().update(
            fileId=file_id,
            addParents=parentID,
            removeParents=previous_parents,
            fields='id, parents,webViewLink'
            ).execute()
            return file['webViewLink'] 
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
            'https://www.googleapis.com/auth/drive.appdata',
            'https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.metadata',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.settings.basic'
        ]
        try:

            print("token exists?========>",os.path.exists('spyproj/token_gdrive.json'))
            if os.path.exists('spyproj/token_gdrive.json'):
                creds = Credentials.from_authorized_user_file('spyproj/token_gdrive.json', SCOPES)

            if not creds or not creds.valid:
                #print("cred not valied 1t if")
                if creds and creds.expired and creds.refresh_token:
                    #print("going to refresh (cred expired) 2nd if")
                    creds.refresh(Request())
                else:
                    #print("cred not expired")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'spyproj/client_secret_gdrive.json', SCOPES)
                    creds = flow.run_console()
        
            with open('spyproj/token_gdrive.json', 'w') as token:
                token.write(creds.to_json())


            #return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
            service = build('drive', 'v3', credentials=creds)
            print("Gdrive AUTH COOOOOOOOOMpleted")
        except Exception as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
        return service
    
    
    def createRemoteFolder(self, folderName,serviceName, parentID):
        
        #print("======>in create folder1")
        folderlist=serviceName.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          ).execute()
        
        titlelist = folderlist.get('files', [])
        #print('**********',str(titlelist))
        for item in titlelist:
            if item['name']==folderName:
                #print("*****======>in create folder existsss============", folderName)
                #print("*****======>in create folder existsss============", item['id'])
                return item['id']
        file_metadata = {
            'name': folderName,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parentID]
        }
        #print("======>in create folder 22", folderName)
        #print("======>in create folder 33", parentID)
        file = serviceName.files().create(body=file_metadata, fields='id').execute()
        #print("======>in create folder completed")
        return file['id']

    def convertVideoAndUpload(self):
        try:
            print('Start convert')
            drive=self.aut()
            folderlist=drive.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          ).execute()
            print('Start convert 2')
            titlelist = folderlist.get('files', [])
            print('Start convert 3 :', titlelist)
            for item in titlelist:
                print('name:', item['name'])
                if item['name']=='kamal':
                    # cameracursor = CameraDetails.find_camera_details_by_params({'building_name':'HORIZON'})
                    # cameralist = list(cameracursor)
                    # #print('No of records in camera:', len(cameralist))
                    # camera_data = cameralist[0]    
                    # url = cam_name = ''
                    # group_name = camera_data['group_name']
                    # building_name = camera_data['building_name']
                    # url = camera_data['url_or_ip_address']
                    # cam_name = camera_data['cam_name']
                    # email_address = camera_data['email_address']
                    # phone_numbers = camera_data['phone_numbers']
                    print("*Done---******",item['name'])
                    results = drive.files().list(q = "'" + item['id'] + "' in parents", fields="nextPageToken, files(*)").execute()
                    items = results.get('files', [])
                    #dirpath = 'D:\\Gopi\\corenuts\\Camera\\AI-main'
                    # tobeInserted =True
                    # tobeUpdated =True
                    for fileItem in items:
                        
                        #thread = Thread(target=self.processdvr, args=([fileItem,drive]), daemon=True)
                        #thread.start()
                        self.processdvr(fileItem,drive)
                        
        except HttpError as error:
            print(f'An error occurred: {error}')

    def processdvr(self, fileItem,drive):
        try:    
            print("*********---******",fileItem['name']  )
            file_id=fileItem['id']
            # if(tobeInserted):
            #     self.insertAlertDetailsIntoDB(group_name,cam_name,building_name,fileItem['name'] ,email_address,phone_numbers)
            #     tobeInserted = False
            request = drive.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            print("* 222********---******" )
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                #print("Download %d%%." % int(status.progress() * 100))

            fh.seek(0)
            # Write the received data to the file
            downloadedFile = os.path.join('', fileItem['name'])
            with open(downloadedFile, 'wb') as f:
                shutil.copyfileobj(fh, f)

            outputFile1 = os.path.join('', fileItem['name'].replace("dav", "mp4" ))
            print("outputFile1::", outputFile1)
            #method 2
            stream = ffmpeg.input(downloadedFile,f='h264')
            stream = ffmpeg.output(stream, outputFile1 )
            ffmpeg.run(stream)
            
            #command =  'ffmpeg.exe -f h264 -i '+ downloadedFile + ' -c copy '+ outputFile1
            #subprocess.run(command)
            time.sleep(180)
            gLink=self.upload(outputFile1,fileItem['name'].replace("dav", "mp4"))
            print("completed upload")
            print(gLink)
             
            self.move(file_id=file_id,destFolder="processedVideos")   
            #if os.path.isfile(outputFile1):
            ##    os.remove(outputFile1)
                #print(gLink)
            if os.path.isfile(downloadedFile):
                os.remove(downloadedFile)
                print(gLink)
            self.createCameraDetailsRecord(outputFile1, gLink)
        except HttpError as error:
            print(f'An error occurred: {error}')

    def createCameraDetailsRecord(self, outputFile1, gLink):
        print("gLink===========>", gLink)
        filter_value = CameraDetailsData.populate_filter('SBR','HORIZON', '', '')
        print('--------------------------------------------------')
        print('filter_value:', filter_value)
            #Insert into DB
        cameracursor = CameraDetails.find_camera_details_by_params(filter_value)
        #cameracursor = CameraDetails.find_camera_details_by_params({'building_name':'HORIZON'})
        cameralist = list(cameracursor)
        #print('No of records in camera:', len(cameralist))
        camera_data = cameralist[0]
        newCameraDetailsData = {}
        newCameraDetailsData['group_name'] = camera_data['group_name']
        newCameraDetailsData['building_name'] = camera_data['building_name']
        newCameraDetailsData['email_address'] = camera_data['email_address']
        newCameraDetailsData['phone_numbers'] = camera_data['phone_numbers']
        newCameraDetailsData['cam_location'] = camera_data['cam_location']
        newCameraDetailsData['monday_starttime'] = camera_data['monday_starttime']
        newCameraDetailsData['monday_nextday_endtime'] = camera_data['monday_nextday_endtime']
        newCameraDetailsData['tuesday_starttime'] = camera_data['tuesday_starttime']
        newCameraDetailsData['tuesday_nextday_endtime'] = camera_data['tuesday_nextday_endtime']
        newCameraDetailsData['wednesday_starttime'] = camera_data['wednesday_starttime']
        newCameraDetailsData['wednesday_nextday_endtime'] = camera_data['wednesday_nextday_endtime']
        newCameraDetailsData['thursday_starttime'] = camera_data['thursday_starttime']
        newCameraDetailsData['thursday_nextday_endtime'] = camera_data['thursday_nextday_endtime']
        newCameraDetailsData['friday_starttime'] = camera_data['friday_starttime']
        newCameraDetailsData['friday_nextday_endtime'] = camera_data['friday_nextday_endtime']
        newCameraDetailsData['saturday_starttime'] = camera_data['saturday_starttime']
        newCameraDetailsData['saturday_nextday_endtime'] = camera_data['saturday_nextday_endtime']
        newCameraDetailsData['sunday_starttime'] = camera_data['sunday_starttime']
        newCameraDetailsData['sunday_nextday_endtime'] = camera_data['sunday_nextday_endtime']

        newCameraDetailsData['url_or_ip_address'] = outputFile1
        newCameraDetailsData['cam_name'] = 'DVR_' + str(datetime.now())
        newCameraDetailsData['run_status'] = 'not running'
        newCameraDetailsData['dvr_flag'] = 'yes'
        newCameraDetailsData['dvr_location_link'] = gLink

        CameraDetails.create_camera(newCameraDetailsData)
        print('Camera Details Created successfully')

    def UpdateAlertDetailsIntoDB(self, group_name,cam_name,building_name,save_path,gLink) :
    	
        #to get unique id
        print("gLink===========>", gLink)
        #save_path=save_path.replace("\\","abcd")
        gLink
        alertName =group_name+cam_name+building_name+ save_path
        #print("filter condition*******",alertName)
        alertcursor = AlertDetails.find_alert_details_by_filterCondition({'alert_name': alertName})
        alertlist = list(alertcursor)
        #print('No of records in UpdateAlertDetailsIntoDB Notification:', len(alertlist))
        for alertData in alertlist:
            alertData['status']='ready'
            alertData['url']=gLink
            alertData = {"$set": alertData}
            AlertDetails.update_alert({'alert_name': alertName}, alertData)
        #print('Alert Update DB completed')       

    def insertAlertDetailsIntoDB(self, group_name,cam_name,building_name,save_path,email_address,phone_numbers) :
            #print("person detected -- Insert cam info into db")
            alertData = {}
            alertData['org_name'] = group_name
            alertData['camera_name'] = cam_name
            alertData['camera_location'] = building_name
            alertData['alert_time'] = datetime.now()
            #save_path=save_path.replace("\\","abcd")
            alertData['video_location'] = save_path
            alertName =alertData['alert_name']=alertData['org_name']+alertData['camera_name']+alertData['camera_location']+ alertData['video_location'] 
            alertData['alert_name']=alertName
            alertData['status']='inprogress'
            alertData['email_address']=email_address
            alertData['phone_numbers']=phone_numbers
            alertData['message_status']='not send'
            alertData['notification_link_status']='not send'
            alertcursor = AlertDetails.find_alert_details_by_filterCondition({'alert_name': alertName})
            #print("************$$$$$$$$$$$$ ALREDAY ALERT IS AVIALBLE $$$$$$$$$$$$$$$$")
            alertlist = list(alertcursor)
            if len(alertlist) == 0:
                #print("insert db=",alertData )
                AlertDetails.create_alert(alertData)
                #print('Insert DB completedddd',alertData)


    def sendEmail(self,gLink,email_address,camera_location):
        try:
            gmail = Gmail()
           
            # Write Logic to send whatapp, email message to customer
            params = {
                "to": email_address,
                "sender": "kamal.corenuts@gmail.com",
                "subject": "Alert(3) - " + camera_location + " Suspicious Activity",
                "msg_html": "<h1>We Identified Suspicious Activity in "+ camera_location + "  !</h1><br />Pls Take the Nescessary action.<video width='320' height='240' controls> <source src="+gLink+" type='video/webm'></video>"+ gLink,
                "signature": True  # use my account signature
            }
            #pip install lxml
            #print("before gmaillllllllllllllllllllll")
            message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)
            
        except Exception as error:
            print(f'An error occurred: {error}')
