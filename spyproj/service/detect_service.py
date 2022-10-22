import datetime
from spyproj import app
from spyproj.yolov7.detect_objects import Detective
from spyproj.service.camera_service import Camera_Service

class Detect_Service:
    def __init__(self):
        print('detect service constructor')
        # d = Detective()
        # print('DETCTIVE')
        # d.detect_object_method()
    
    def __isEligibleForProcess(self, camera_data):
        print(camera_data)
        today_week_name = str(datetime.datetime.now().strftime('%A').lower())
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
            todays_date = datetime.datetime.now()
            todays_date = todays_date.replace(second=00, microsecond=0)
            #run_date = todays_date.replace(hour=int(timestr_arr[0]), minute=int(timestr_arr[1]))
            run_date = todays_date.replace(hour=11, minute=int(timestr_arr[1]))
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

    def run_detect_process(self):
        print('Process all cams')

        #1. Get all the Camera details
        cameralist = Camera_Service.find_camera_details_by_nonrunning_status()
        for camera_data in cameralist:
            isRun = self.__isEligibleForProcess(camera_data)
            if (isRun is True):
                url = cam_name = ''
                if 'url_or_ip_address' in camera_data:
                    print(camera_data['url_or_ip_address'])
                    url = camera_data['url_or_ip_address']
                if 'cam_name' in camera_data:
                    print('Cam name:', camera_data['cam_name'])
                    cam_name = camera_data['cam_name']

                print('Run detect method:', url, ' Came name:' , cam_name )
            else:
                print('Dont run')


        # finally invoke
        # d = Detective()
        # print('DETCTIVE')
        # d.detect_object_method()
    
    





