import os
from datetime import datetime, timedelta
import time
from threading import Thread
from spyproj import app
from flask import Flask
from flask_apscheduler import APScheduler
from spyproj.yolov7.detect_objects import Detective
from spyproj.service.camera_service import Camera_Service

#subscheduler = APScheduler()
#subscheduler.start()

class Detect_Service:
    def __init__(self):
        print('detect service constructor')
        # d = Detective()
        # print('DETCTIVE')
        # d.detect_object_method()
    
    def __isEligibleForProcess(self, camera_data):
        print(camera_data)
        today_week_name = str(datetime.now().strftime('%A').lower())
        # get weekday name
        print('day Name:', today_week_name)
        timestr =''
        if 'monday_starttime' in camera_data:
            print(camera_data['monday_starttime'])
            value = str("monday_starttime")
            #print(type(value))
            if today_week_name in value:
                print('monday_starttime:', camera_data['monday_starttime'])
                timestr = camera_data['monday_starttime']
            
        if 'tuesday_starttime' in camera_data:
            print(camera_data['tuesday_starttime'])
            value = str("tuesday_starttime")
            if today_week_name in value:
                print('tuesday_starttime:', camera_data['tuesday_starttime'])
                timestr = camera_data['tuesday_starttime']

        if 'wednesday_starttime' in camera_data:
            print(camera_data['wednesday_starttime'])
            value = str("wednesday_starttime")
            if today_week_name in value:
                print('wednesday_starttime:', camera_data['wednesday_starttime'])
                timestr = camera_data['wednesday_starttime']

        if 'thursday_starttime' in camera_data:
            print(camera_data['thursday_starttime'])
            value = str("thursday_starttime")
            if today_week_name in value:
                print('thursday_starttime:', camera_data['thursday_starttime'])
                timestr = camera_data['thursday_starttime']

        if 'friday_starttime' in camera_data:
            print(camera_data['friday_starttime'])
            value = str("friday_starttime")
            if today_week_name in value:
                print('friday_starttime:', camera_data['friday_starttime'])
                timestr = camera_data['friday_starttime']
        
        if 'saturday_starttime' in camera_data:
            print(camera_data['saturday_starttime'])
            value = str("saturday_starttime")
            if today_week_name in value:
                print('saturday_starttime:', camera_data['saturday_starttime'])
                timestr = camera_data['saturday_starttime']

        if 'sunday_starttime' in camera_data:
            print(camera_data['sunday_starttime'])
            value = str("sunday_starttime")
            if today_week_name in value:
                print('sunday_starttime:', camera_data['sunday_starttime'])
                timestr = camera_data['sunday_starttime']

        if (timestr != ''):
            print('timestr', timestr)
            timestr_arr = timestr.split(":")
            print('timestr_arr', timestr_arr)
            print("timestr_min", timestr_arr[0])
            print("timestr_sec", timestr_arr[1])
            todays_date = datetime.now()
            todays_date = todays_date.replace(second=00, microsecond=0)
            run_date = todays_date.replace(hour=int(timestr_arr[0]), minute=int(timestr_arr[1]))
            #run_date = todays_date.replace(hour=11, minute=int(timestr_arr[1]))
            print('todays_date', todays_date)
            print('run_date', run_date)

            if run_date <= todays_date:
                print('HAI')
                return True
            else:
                print('BYE')
                return False
        else:
            print('No Object')
            return False

    def __get_process_endtime(self, camera_data):
        print(camera_data)
        today_week_name = str(datetime.now().strftime('%A').lower())
        # get weekday name
        print('day Name:', today_week_name)
        timestr =''
        if 'monday_nextday_endtime' in camera_data:
            print(camera_data['monday_nextday_endtime'])
            value = str("monday_nextday_endtime")
            #print(type(value))
            if today_week_name in value:
                print('monday_nextday_endtime:', camera_data['monday_nextday_endtime'])
                timestr = camera_data['monday_nextday_endtime']
            
        if 'tuesday_nextday_endtime' in camera_data:
            print(camera_data['tuesday_nextday_endtime'])
            value = str("tuesday_nextday_endtime")
            if today_week_name in value:
                print('tuesday_nextday_endtime:', camera_data['tuesday_nextday_endtime'])
                timestr = camera_data['tuesday_nextday_endtime']

        if 'wednesday_nextday_endtime' in camera_data:
            print(camera_data['wednesday_nextday_endtime'])
            value = str("wednesday_nextday_endtime")
            if today_week_name in value:
                print('wednesday_nextday_endtime:', camera_data['wednesday_nextday_endtime'])
                timestr = camera_data['wednesday_nextday_endtime']

        if 'thursday_nextday_endtime' in camera_data:
            print(camera_data['thursday_nextday_endtime'])
            value = str("thursday_nextday_endtime")
            if today_week_name in value:
                print('thursday_nextday_endtime:', camera_data['thursday_nextday_endtime'])
                timestr = camera_data['thursday_nextday_endtime']

        if 'friday_nextday_endtime' in camera_data:
            print(camera_data['friday_nextday_endtime'])
            value = str("friday_nextday_endtime")
            if today_week_name in value:
                print('friday_nextday_endtime:', camera_data['friday_nextday_endtime'])
                timestr = camera_data['friday_nextday_endtime']
        
        if 'saturday_nextday_endtime' in camera_data:
            print(camera_data['saturday_nextday_endtime'])
            value = str("saturday_nextday_endtime")
            if today_week_name in value:
                print('saturday_nextday_endtime:', camera_data['saturday_nextday_endtime'])
                timestr = camera_data['saturday_nextday_endtime']

        if 'sunday_nextday_endtime' in camera_data:
            print(camera_data['sunday_nextday_endtime'])
            value = str("sunday_nextday_endtime")
            if today_week_name in value:
                print('sunday_nextday_endtime:', camera_data['sunday_nextday_endtime'])
                timestr = camera_data['sunday_nextday_endtime']

        next_date = datetime.now() + timedelta(1)
        print('intiiallu next_date', next_date)
        if (timestr != ''):
            print('END PORECC timestr', timestr)
            timestr_arr = timestr.split(":")
            print('timestr_arr', timestr_arr)
            print("timestr_min", timestr_arr[0])
            print("timestr_sec", timestr_arr[1])
            next_date = next_date.replace(hour=int(timestr_arr[0]), minute=int(timestr_arr[1]), second=00, microsecond=0)
            print('final next_date', next_date)

        return next_date


    def run_detect_process(self):
        print('Process all cams')

        #1. Get all the Camera details
        cameralist = Camera_Service.find_camera_details_by_nonrunning_status()
        for camera_data in cameralist:
            isRun = self.__isEligibleForProcess(camera_data)
            
            if (isRun is True):
                url = cam_name = dvr_location_link = dvr_flag = ''
                if 'group_name' in camera_data:
                    print('group_name:', camera_data['group_name'])
                    group_name = camera_data['group_name']
                if 'building_name' in camera_data:
                    print('building_name:', camera_data['building_name'])
                    building_name = camera_data['building_name']
                if 'url_or_ip_address' in camera_data:
                    print(camera_data['url_or_ip_address'])
                    url = camera_data['url_or_ip_address']
                if 'cam_name' in camera_data:
                    print('Cam name:', camera_data['cam_name'])
                    cam_name = camera_data['cam_name']
                if 'email_address' in camera_data:
                    print('Email Address:', camera_data['email_address'])
                    email_address = camera_data['email_address']
                if 'phone_numbers' in camera_data:
                    print('Phone Numbers:', camera_data['phone_numbers'])
                    phone_numbers = camera_data['phone_numbers']
                if 'dvr_flag' in camera_data:
                    print('dvr_flag:', camera_data['dvr_flag'])
                    dvr_flag = camera_data['dvr_flag']
                if 'dvr_location_link' in camera_data:
                    print('dvr_location_link:', camera_data['dvr_location_link'])
                    dvr_location_link = camera_data['dvr_location_link']

                # get end time from camera detail table
                process_endtime = self.__get_process_endtime(camera_data)
                print('process_endtime:::', process_endtime)

                print('Run detect method:', url, ' Came name:' , cam_name , ' group_name:' , group_name, ' building_name:' , building_name, ' email_address:' , email_address, ' phone_numbers:' , phone_numbers )
                d = Detective()

                # Create History
                Camera_Service.create_camera_history(group_name, building_name, cam_name)
                # Update Camera Details with status
                Camera_Service.update_camera_status_as_running(group_name, building_name, cam_name)
                print('DETCTIVE')
                d.detect_process(url, process_endtime,group_name,cam_name,building_name,email_address,phone_numbers,dvr_flag,dvr_location_link)
                print('Break Done')
                Camera_Service.update_camera_history(group_name, building_name, cam_name)
                print('All Done')
                return
            else:
                print('Dont run ')
                return
    
    def run_detect_processes(self):
        print('Process all cams')

        #1. Get all the Camera details
        cameralist = Camera_Service.find_camera_details_by_nonrunning_status()
        count =1
        for camera_data in cameralist:
            isRun = self.__isEligibleForProcess(camera_data)
            
            if (isRun is True):
                print('Condition satisfied:----------------------------', count)
                count=count+1
                #next_date = datetime.now() + timedelta(seconds=3)
                #print('new_Date:', next_date)
                #schedulerName = 'subscheduler'+str(count)
                #schedulerName = APScheduler()
                #subscheduler.add_job(id='Schedule1', func= abcMethod, trigger = 'cron', hour = '*', minute = '*/1')
                #subscheduler.add_job(id='Schedule Task For Detects', func=schedulerTaskFor, args= ['HAI'], trigger = 'cron', hour = '*', minute = '*', second = '*/10')
                #jobname = 'hellotest_'+ str(count)
                #schedulerName.add_job(id = jobname, func=processCameras, trigger='interval', args= [camera_data], end_date =next_date)
                #schedulerName.start()
                
                #thread = Thread(target=self.processCameras, args=([camera_data]), daemon=True)
                #thread.start()
                
                self.processCameras(camera_data)
                #return
            else:
                print('Dont run')
                #return

    def processCameras(self, camera_data):
        print('test method:')
        url = cam_name = dvr_location_link = dvr_flag = ''
        if 'group_name' in camera_data:
            print('group_name:', camera_data['group_name'])
            group_name = camera_data['group_name']
        if 'building_name' in camera_data:
            print('building_name:', camera_data['building_name'])
            building_name = camera_data['building_name']
        if 'url_or_ip_address' in camera_data:
            print(camera_data['url_or_ip_address'])
            url = camera_data['url_or_ip_address']
        if 'cam_name' in camera_data:
            print('Cam name:', camera_data['cam_name'])
            cam_name = camera_data['cam_name']
        if 'email_address' in camera_data:
            print('Email Address:', camera_data['email_address'])
            email_address = camera_data['email_address']
        if 'phone_numbers' in camera_data:
            print('Phone Numbers:', camera_data['phone_numbers'])
            phone_numbers = camera_data['phone_numbers']
        if 'dvr_flag' in camera_data:
            print('dvr_flag:', camera_data['dvr_flag'])
            dvr_flag = camera_data['dvr_flag']
        if 'dvr_location_link' in camera_data:
            print('dvr_location_link:', camera_data['dvr_location_link'])
            dvr_location_link = camera_data['dvr_location_link']

        # get end time from camera detail table
        process_endtime = self.__process_endtime(camera_data)
        print('process_endtime:::', process_endtime)

        print('Run detect method:', url, ' Came name:' , cam_name , ' group_name:' , group_name, ' building_name:' , building_name, ' email_address:' , email_address, ' phone_numbers:' , phone_numbers )
        d = Detective()

        # Create History
        Camera_Service.create_camera_history(group_name, building_name, cam_name)
        # Update Camera Details with status
        Camera_Service.update_camera_status_as_running(group_name, building_name, cam_name)
        print('DETCTIVE')
        d.detect_process(url, process_endtime,group_name,cam_name,building_name,email_address,phone_numbers,dvr_flag,dvr_location_link)
        print('Break Done')
        Camera_Service.update_camera_history(group_name, building_name, cam_name)
        print('All Done')

    def __process_endtime(self, camera_data):
        print(camera_data)
        today_week_name = str(datetime.now().strftime('%A').lower())
        # get weekday name
        print('day Name:', today_week_name)
        timestr =''
        if 'monday_nextday_endtime' in camera_data:
            print(camera_data['monday_nextday_endtime'])
            value = str("monday_nextday_endtime")
            #print(type(value))
            if today_week_name in value:
                print('monday_nextday_endtime:', camera_data['monday_nextday_endtime'])
                timestr = camera_data['monday_nextday_endtime']
            
        if 'tuesday_nextday_endtime' in camera_data:
            print(camera_data['tuesday_nextday_endtime'])
            value = str("tuesday_nextday_endtime")
            if today_week_name in value:
                print('tuesday_nextday_endtime:', camera_data['tuesday_nextday_endtime'])
                timestr = camera_data['tuesday_nextday_endtime']

        if 'wednesday_nextday_endtime' in camera_data:
            print(camera_data['wednesday_nextday_endtime'])
            value = str("wednesday_nextday_endtime")
            if today_week_name in value:
                print('wednesday_nextday_endtime:', camera_data['wednesday_nextday_endtime'])
                timestr = camera_data['wednesday_nextday_endtime']

        if 'thursday_nextday_endtime' in camera_data:
            print(camera_data['thursday_nextday_endtime'])
            value = str("thursday_nextday_endtime")
            if today_week_name in value:
                print('thursday_nextday_endtime:', camera_data['thursday_nextday_endtime'])
                timestr = camera_data['thursday_nextday_endtime']

        if 'friday_nextday_endtime' in camera_data:
            print(camera_data['friday_nextday_endtime'])
            value = str("friday_nextday_endtime")
            if today_week_name in value:
                print('friday_nextday_endtime:', camera_data['friday_nextday_endtime'])
                timestr = camera_data['friday_nextday_endtime']
        
        if 'saturday_nextday_endtime' in camera_data:
            print(camera_data['saturday_nextday_endtime'])
            value = str("saturday_nextday_endtime")
            if today_week_name in value:
                print('saturday_nextday_endtime:', camera_data['saturday_nextday_endtime'])
                timestr = camera_data['saturday_nextday_endtime']

        if 'sunday_nextday_endtime' in camera_data:
            print(camera_data['sunday_nextday_endtime'])
            value = str("sunday_nextday_endtime")
            if today_week_name in value:
                print('sunday_nextday_endtime:', camera_data['sunday_nextday_endtime'])
                timestr = camera_data['sunday_nextday_endtime']

        next_date = datetime.now() + timedelta(1)
        print('intiiallu next_date', next_date)
        if (timestr != ''):
            print('END PORECC timestr', timestr)
            timestr_arr = timestr.split(":")
            print('timestr_arr', timestr_arr)
            print("timestr_min", timestr_arr[0])
            print("timestr_sec", timestr_arr[1])
            next_date = next_date.replace(hour=int(timestr_arr[0]), minute=int(timestr_arr[1]), second=00, microsecond=0)
            print('final next_date', next_date)

        return next_date



def schedulerTaskFor(argument):
    print('test method:', argument)




