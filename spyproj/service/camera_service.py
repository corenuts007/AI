import datetime

from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.cameradetails_repository import CameraDetails
from spyproj.model.camera_details_data import CameraDetailsData
from spyproj.repository.camerahistory_repository import CameraHistory
from spyproj.model.camera_history_data import CameraHistoryData
from flask import jsonify
from bson.objectid import ObjectId

class Camera_Service:
    def find_camera_details_by_running_status():
        try:
            # find method returns cursor object
            
            cameracursor = CameraDetails.get_camera_details_bystatus({'run_status':'running'})
            cameralist = list(cameracursor)
            print('No of records in camera:', len(cameralist))
            return cameralist
 
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())
    
    def find_camera_details_by_nonrunning_status():
        try:
            # find method returns cursor object
            
            cameracursor = CameraDetails.get_camera_details_bystatus({'run_status':'not running'})
            cameralist = list(cameracursor)
            print('No of records in camera:', len(cameralist))
            return cameralist
 
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())
    
    def update_camera_status_as_running(group_name, building_name, cam_name):
        try:
            # find method returns cursor object
            
             #find the existing camera details whose status is not running
            filter_value = CameraDetailsData.populate_filter(group_name, building_name, cam_name, 'not running')
            print('--------------------------------------------------')
            print('filter_value:', filter_value)
            #Insert into DB
            cameracursor = CameraDetails.find_camera_details_by_params(filter_value)
            cameralist = list(cameracursor)
            print('No of records in camera:', len(cameralist))
            update_data = cameralist[0]
            # update_data = ''
            # for camera_data in cameralist:
            #     if 'endtime' in camera_data:
            #         endtime = camera_data['endtime']
            #         print('end time:', endtime)
            #         if endtime == '':
            #             update_data = camera_data
            #             break
            #update_data.endtime = datetime.datetime.today()
            update_data['run_status'] = 'running'
            #print('Update:', update_data)
            #print('ID-------ccc------:', update_data['_id'])
            filter_id = {'_id': ObjectId(update_data['_id'])}
            print('Filter Id:', filter_id)
            update_data = {"$set": update_data}
            #print('update_data Id:', update_data)
            CameraDetails.update_camera(filter_id, update_data)
            #return cameralist
            return
 
        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())

    def create_camera_history(group_name, building_name, cam_name):
        try:
            
            #Create object for camera history data
            create_data = CameraHistoryData(group_name, building_name, cam_name, datetime.datetime.today(), '')
            new_data = CameraHistoryData.camera_history_data(create_data)
            print('create_data:', new_data)
            #Insert into DB
            CameraHistory.create_camera_history(new_data)
            return

        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())

    def update_camera_history(group_name, building_name, cam_name):
        try:
            # find method returns cursor object
            
             #Create object for camera history data
            filter_value = CameraHistoryData.populate_filter(group_name, building_name, cam_name)
            print('--------------------------------------------------')
            print('filter_value:', filter_value)
            #find the history records, FIXME, here need to pass endtime as null filter
            cameracursor = CameraHistory.find_camera_history_by_params(filter_value)
            cameralist = list(cameracursor)
            #print('No of records in camera:', len(cameralist))
            #print('Data:', cameralist[0])
            update_data = ''
            for camera_data in cameralist:
                if 'endtime' in camera_data:
                    endtime = camera_data['endtime']
                    #print('end time:', endtime)
                    if endtime == '':
                        update_data = camera_data
                        break
            
            #print('update_data:', update_data)
            update_data['endtime'] = datetime.datetime.today()
            #print('Update:', update_data)
            #print('ID-------ccc------:', update_data['_id'])
            filter_id = {'_id': ObjectId(update_data['_id'])}
            #print('Filter Id:', filter_id)
            update_data = {"$set": update_data}
            #print('update_data Id:', update_data)
            CameraHistory.update_camera_history(filter_id, update_data)
            #return cameralist
            return

        except Exception as ex:
            print("*Exception*", ex)
            print(ex.__str__())
