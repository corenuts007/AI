from spyproj.service.detect_service import Detect_Service
from spyproj.service.alert_service import Alert_Service
from flask import jsonify
class Schedule_jobs:

    def detect_scheduler_task():
        print('welcome schedulerTasks')
        detect = Detect_Service()
        detect.run_detect_process()
        return
    
    def alert_message_scheduler_task():
        print('welcome alert_message_scheduler_task')
        alert = Alert_Service()
        alert.alert_message_process()
        return

    def alert_notification_scheduler_task():
        print('welcome alert_notification_scheduler_task')
        alert = Alert_Service()
        alert.alert_notification_process()
        return
