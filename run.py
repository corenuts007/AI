import os
import datetime
from spyproj import app
from flask import Flask
from flask_apscheduler import APScheduler
from spyproj.scheduler.schedulejobs import Schedule_jobs
from loguru import logger

scheduler = APScheduler()

def schedulerTaskForDetect():
    dt = datetime.datetime.now()

    print('Method Entry: schedulerTaskForDetect @', datetime.datetime.today())
    Schedule_jobs.detect_scheduler_task()
    print('Method Exit: schedulerTaskForDetect @', datetime.datetime.today())

def schedulerTaskForAlertMessage():
    dt = datetime.datetime.now()

    print('Method Entry: schedulerTaskForAlertMessage @', datetime.datetime.today())
    Schedule_jobs.alert_message_scheduler_task()
    print('Method Exit: schedulerTaskForAlertMessage @', datetime.datetime.today())

def schedulerTaskForAlertNotification():
    dt = datetime.datetime.now()

    print('Method Entry: schedulerTaskForAlertNotification @', datetime.datetime.today())
    Schedule_jobs.alert_notification_scheduler_task()
    print('Method Exit: schedulerTaskForAlertNotification @', datetime.datetime.today())

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    
    logger.add(
        'logs/myapp.log',
        level='DEBUG',
        format='{time} {level} {message}',
        backtrace=True,
        rotation='5 MB',
        retention=9
    )
    logger.debug("Logger started in run.py")
    print('scheduler task for Detected started')
    # Scheduled the trigger as per requirement. This is place to run the schedular automatically once service is up
    #scheduler.add_job(id='Schedule Task', func= schedulerTaskForDetect, trigger = 'cron', hour = '*', minute = '00,10,20,30,40,55')
    
    # Trigger Defect service for every 10 mins (Cam service run based on configuration from Camera Detail table)
    scheduler.add_job(id='Schedule Task For Detect', func= schedulerTaskForDetect, trigger = 'cron', hour = '*', minute = '*/1')
    
    # Trigger Alert Message service for every 2 mins (Send email, whatapp message to Customer from Alert Detail table)
    scheduler.add_job(id='Schedule Task For Alert Message', func= schedulerTaskForAlertMessage, trigger = 'cron', hour = '*', minute = '*/1')
    
    # Trigger Alert Notification service for every 5 mins(Send vedio links via email/whatapp to Customer from Alert Detail table)
    scheduler.add_job(id='Schedule Task For Alert Notification', func= schedulerTaskForAlertNotification, trigger = 'cron', hour = '*', minute = '*/1')
    scheduler.start()

    app.run(debug=False, host='0.0.0.0', port=int(port))
