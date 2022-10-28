import datetime

from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.alertdetails_repository import AlertDetails
from spyproj.model.alert_details_data import AlertDetailsData
from bson.objectid import ObjectId

class Alert_Service:
    def alert_message_process(self):
        try:
            # find method returns cursor object
            print('Method entry: Alert Message')
            alertcursor = AlertDetails.find_alert_details_by_status({'status':'inprogress', 'message_status':'not send'})
            alertlist = list(alertcursor)
            print('No of records in ALERT message:', len(alertlist))
            for alert_data in alertlist:
                if 'group_name' in alert_data:
                    print('group_name:', alert_data['group_name'])
                    group_name = alert_data['group_name']
                if 'building_name' in alert_data:
                    print('building_name:', alert_data['building_name'])
                    building_name = alert_data['building_name']
                if 'camera_name' in alert_data:
                    print('camera_name:', alert_data['camera_name'])
                    camera_name = alert_data['camera_name']

                # Write Logic to send whatapp, email message to customer

                # Update Alert table with Message status as 'Sent'
                self.__update_alert_message_status(alert_data)
            print('Method Exit: Alert Message')
            return
 
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())


    def alert_notification_process(self):
        print('Method entry: Alert Notification')
        try:
            # find method returns cursor object
            
            alertcursor = AlertDetails.find_alert_details_by_status({'status':'ready','notification_link_status':'not send'})
            alertlist = list(alertcursor)
            print('No of records in ALERT Notification:', len(alertlist))
            for alert_data in alertlist:
                if 'group_name' in alert_data:
                    print('group_name:', alert_data['group_name'])
                    group_name = alert_data['group_name']
                if 'building_name' in alert_data:
                    print('building_name:', alert_data['building_name'])
                    building_name = alert_data['building_name']
                if 'camera_name' in alert_data:
                    print('camera_name:', alert_data['camera_name'])
                    camera_name = alert_data['camera_name']
                # Write Logic to send notification link to customer

                # Update Alert table with notification status as 'Sent'
                self.__update_alert_notification_status(alert_data)
            print('Method Exit: Alert Notification')
            return
 
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())



    def __update_alert_message_status(self, alert_data):
        try:
            print('Method Entry: __update_alert_message_status')

            alert_data['message_status'] = 'sent'
            #print('Update:', update_data)
            #print('ID-------ccc------:', update_data['_id'])
            filter_id = {'_id': ObjectId(alert_data['_id'])}
            print('Filter Id:', filter_id)
            update_data = {"$set": alert_data}
            #print('update_data Id:', update_data)
            AlertDetails.update_alert(filter_id, update_data)
            #return cameralist
            print('Method Exit: __update_alert_message_status')
            return
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())

    def __update_alert_notification_status(self, alert_data):
        try:
            print('Method Entry: __update_alert_notification_status')

            alert_data['notification_link_status'] = 'sent'
            #print('Update:', update_data)
            #print('ID-------ccc------:', update_data['_id'])
            filter_id = {'_id': ObjectId(alert_data['_id'])}
            print('Filter Id:', filter_id)
            update_data = {"$set": alert_data}
            #print('update_data Id:', update_data)
            AlertDetails.update_alert(filter_id, update_data)
            print('Method Exit: __update_alert_notification_status')
            return
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())

