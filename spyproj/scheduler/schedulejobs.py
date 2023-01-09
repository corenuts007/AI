from spyproj.service.detect_service import Detect_Service
from spyproj.service.alert_service import Alert_Service
from spyproj.service.gauth_service import Gauth_Service
from flask import jsonify
class Schedule_jobs:

    def detect_scheduler_task():
        print('Method Entry: Schedule_jobs - detect_scheduler_task')
        detect = Detect_Service()
        detect.run_detect_process()
        print('Method Exit: Schedule_jobs - detect_scheduler_task')
        return
    
    def detect_scheduler_tasks():
        print('Method Entry: Sched  ule_jobs - detect_scheduler_tasks')
        detect = Detect_Service()
        detect.run_detect_processes()
        print('Method Exit: Schedule_jobs - detect_scheduler_tasks')
        return
    
    def alert_message_scheduler_task():
        print('Method Entry: Schedule_jobs - alert_message_scheduler_task')
        alert = Alert_Service()
        alert.alert_message_process()
        print('Method Exit: Schedule_jobs - alert_message_scheduler_task ')
        return

    def alert_notification_scheduler_task():
        print('Method Entry: Schedule_jobs - alert_notification_scheduler_task')
        alert = Alert_Service()
        alert.alert_notification_process()
        print('Method Exit: Schedule_jobs - alert_notification_scheduler_task')
        return

    def gauth_scheduler_task():
        print('Method Entry: Schedule_jobs - gauth_scheduler_task')
        gauth = Gauth_Service()
        gauth.test_api_request()
        print('Method Exit: Schedule_jobs - gauth_scheduler_task')
        return
        
    def schedulerTaskForProcessDVR():
        print('Method Entry: Schedule_jobs - DVR process task')
        alert = Alert_Service()
        alert.schedulerTaskForProcessDVR()
        print('Method Exit: Schedule_jobs - DVR process task')
        return

