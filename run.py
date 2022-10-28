import os
import datetime
from spyproj import app
from flask import Flask
from flask_apscheduler import APScheduler
from spyproj.scheduler.schedulejobs import Schedule_jobs

scheduler = APScheduler()

def schedulerTaskForDetect():
    dt = datetime.datetime.now()

    print('scheduler task for Detect', datetime.datetime.today())
    #Schedule_jobs.detect_scheduler_task()
    print('scheduler task for Detect Service Completed', datetime.datetime.today())

def schedulerTaskForAlertMessage():
    dt = datetime.datetime.now()

    print('scheduler task for Alert Message', datetime.datetime.today())
    Schedule_jobs.alert_message_scheduler_task()
    print('scheduler task for Alert Message Completed', datetime.datetime.today())

def schedulerTaskForAlertNotification():
    dt = datetime.datetime.now()

    print('scheduler task for Alert Notification', datetime.datetime.today())
    Schedule_jobs.alert_notification_scheduler_task()
    print('scheduler task for Alert Notification Completed', datetime.datetime.today())

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    #app.run(debug=True)
    print('scheduler task')
    # Scheduled the trigger as per requirement. This is place to run the schedular automatically once service is up
    #scheduler.add_job(id='Schedule Task', func= schedulerTaskForDetect, trigger = 'cron', hour = '*', minute = '00,10,20,30,40,55')
    #scheduler.add_job(id='Schedule Task For Detect', func= schedulerTaskForDetect, trigger = 'cron', hour = '*', minute = '*/10')
    scheduler.add_job(id='Schedule Task For Alert Message', func= schedulerTaskForAlertMessage, trigger = 'cron', hour = '*', minute = '*/2')
    scheduler.add_job(id='Schedule Task For Alert Notification', func= schedulerTaskForAlertNotification, trigger = 'cron', hour = '*', minute = '*/5')
    scheduler.start()

    app.run(debug=False, host='0.0.0.0', port=int(port))
