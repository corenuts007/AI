import datetime

from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.alertdetails_repository import AlertDetails
from spyproj.model.alert_details_data import AlertDetailsData
from bson.objectid import ObjectId
from spyproj.utils.googleDriveUpload import googleDriveUpload
from spyproj.utils.simplegmail.gmail import Gmail

class Alert_Service:
    def alert_message_process(self):
        try:
            
            # find method returns cursor object
            print('Method entry: Alert_Service - alert_message_process')
            alertcursor = AlertDetails.find_alert_details_by_filterCondition({'message_status':'not send'})
            alertlist = list(alertcursor)
            print('No of records in ALERT message:', len(alertlist))
            if(len(alertlist)>0):
                gmail = Gmail()
            for alert_data in alertlist:
                if 'group_name' in alert_data:
                    print('group_name:', alert_data['group_name'])
                    group_name = alert_data['group_name']
                if 'camera_location' in alert_data:
                    print('camera_location:', alert_data['camera_location'])
                    camera_location = alert_data['camera_location']
                if 'camera_name' in alert_data:
                    print('camera_name:', alert_data['camera_name'])
                    camera_name = alert_data['camera_name']

                if 'email_address' in alert_data:
                    print('Email Address:', alert_data['email_address'])
                    email_address = alert_data['email_address']
                if 'phone_numbers' in alert_data:
                    print('Phone Numbers:', alert_data['phone_numbers'])
                    phone_numbers = alert_data['phone_numbers']


                # Write Logic to send whatapp, email message to customer
                
                params = {
                    "to": email_address,
                    "sender": "kamal.corenuts@gmail.com",
                    "subject": "Alert - " + camera_location + " Suspicious Activity",
                    "msg_html": "<h1>We Identified   Suspicious Activity in "+ camera_location + "  !</h1><br />Pls Take the Nescessary action.",
                    "msg_plain": " ",
                    "signature": True  # use my account signature
                }
                message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)
                print("mail...",message)

                # Update Alert table with Message status as 'Sent'
                self.__update_alert_message_status(alert_data)
            print('Method Exit: Alert_Service - alert_message_process')
            return
 
        except Exception as ex:
            print("*Exception* in alert_message_process", ex)
            print(ex.__str__())


    def alert_notification_process(self):
        print('Method Entry: Alert_Service - alert_notification_process')
        try:
            # find method returns cursor object
            alertcursor = AlertDetails.find_alert_details_by_filterCondition({'status':'ready','notification_link_status':'not send'})
            alertlist = list(alertcursor)
            print('No of records in ALERT Notification::', len(alertlist))
            if(len(alertlist)>0):
                gmail = Gmail()
            for alert_data in alertlist:
                dvr_flag = ''
                if 'group_name' in alert_data:
                    print('group_name:', alert_data['group_name'])
                    group_name = alert_data['group_name']
                if 'camera_location' in alert_data:
                    print('camera_location:', alert_data['camera_location'])
                    camera_location = alert_data['camera_location']
                if 'camera_name' in alert_data:
                    print('camera_name:', alert_data['camera_name'])
                    camera_name = alert_data['camera_name']

                if 'email_address' in alert_data:
                    print('Email Address:', alert_data['email_address'])
                    email_address = alert_data['email_address']
                if 'phone_numbers' in alert_data:
                    print('Phone Numbers:', alert_data['phone_numbers'])
                    phone_numbers = alert_data['phone_numbers']
                    
                if 'video_location' in alert_data:
                    print('video Locaion:', alert_data['video_location'])
                    video_location = alert_data['video_location']

                if 'dvr_flag' in alert_data:
                    print('dvr_flag:', alert_data['dvr_flag'])
                    dvr_flag = alert_data['dvr_flag']

                if 'url' in alert_data:
                    print('url:', alert_data['url'])
                    url = alert_data['url']
                
                
                # Add the video attachment, if the process is NON-DVR
                #googleDriveUpload
                print("Uploading video into google Drive. video_location: :"+ video_location)
                if dvr_flag=='':
                    gdriveLink = googleDriveUpload()
                    gLink=gdriveLink.upload(video_location,"video_name1")
                    alert_data['url']=gLink  ##update Google drive url into alert table
                else:
                    gLink=url

                # Write Logic to send whatapp, email message to customer
                params = {
                    "to": email_address,
                    "sender": "kamal.corenuts@gmail.com",
                    "subject": "Alert(3) - " + camera_location + " Suspicious Activity",
                    "msg_html": "<h1>We Identified Suspicious Activity in "+ camera_location + "  !</h1><br />Pls Take the Nescessary action.<video width='320' height='240' controls> <source src="+gLink+" type='video/webm'></video>"+ gLink,
                    "signature": True  # use my account signature
                }
                #pip install lxml
                print("before gmaillllllllllllllllllllll")
                message = gmail.send_message(**params)  # equivalent to send_message(to="you@youremail.com", sender=...)
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^Success upoad and mail...",message)
                # Update Alert table with notification status as 'Sent'
                self.__update_alert_notification_status(alert_data)
            print('Method Exit: Alert_Service - alert_notification_process')
            return
 
        except Exception as ex:
            print("*Exception* in alert_notification_process", ex)
            print("13 13 13")
            print(ex.__str__())



    def __update_alert_message_status(self, alert_data):
        try:
            print('Method Entry: Alert_Service - __update_alert_message_status')

            alert_data['message_status'] = 'sent'
            #print('Update:', update_data)
            #print('ID-------ccc------:', update_data['_id'])
            filter_id = {'_id': ObjectId(alert_data['_id'])}
            print('Filter Id:', filter_id)
            update_data = {"$set": alert_data}
            #print('update_data Id:', update_data)
            AlertDetails.update_alert(filter_id, update_data)
            #return cameralist
            print('Method Exit: Alert_Service - __update_alert_message_status')
            return
        except Exception as ex:
            print("*Exception* in __update_alert_message_status", ex)
            print(ex.__str__())

    def __update_alert_notification_status(self, alert_data):
        try:
            print('Method Entry: Alert_Service - __update_alert_notification_status')
            alert_data['notification_link_status'] = 'sent'
            #print('Update:', update_data)
            #print('ID-------ccc------:', update_data['_id'])
            filter_id = {'_id': ObjectId(alert_data['_id'])}
            print('Filter Id:', filter_id)
            update_data = {"$set": alert_data}
            #print('update_data Id:', update_data)
            AlertDetails.update_alert(filter_id, update_data)
            print('Method Exit: Alert_Service - __update_alert_notification_status')
            return
        except Exception as ex:
            print("*Exception in __update_alert_notification_status", ex)
            print(ex.__str__())
    

    def schedulerTaskForProcessDVR(self):
        print('Method Entry: Alert_Service - Process DVR')
        try:
            
            print('Method Entry: Alert_Service - 11111')
            #insertAlertDetailsIntoDB('SBR','01','horizon','save_path','krishnar8@gmail.com','9940085336')

            gdriveLink = googleDriveUpload()
            print('Method Entry: Alert_Service - 2222')
            gdriveLink.convertVideoAndUpload()
 
            print('Method Exit: Alert_Service - Process DVR')
            return
 
        except Exception as ex:
            print("exception in Process DVR method: ", ex)
            print(ex.__str__())


