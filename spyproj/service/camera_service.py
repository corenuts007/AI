from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.cameradetails_repository import CameraDetails
from spyproj.model.camera_details_data import CameraDetailsData
from flask import jsonify

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

