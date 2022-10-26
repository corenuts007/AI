import os
import datetime
from spyproj import app
from flask import Flask
from flask_apscheduler import APScheduler
from spyproj.scheduler.schedulejobs import Schedule_jobs

scheduler = APScheduler()

def schedulerTask():
    dt = datetime.datetime.now()

    print('scheduler task', datetime.datetime.today())
    Schedule_jobs.scheduler_tasks()
    print('scheduler task --2 Completed', datetime.datetime.today())

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    #app.run(debug=True)
    print('scheduler taskffff')
    # Scheduled the trigger as per requirement. This is place to run the schedular automatically once service is up
    scheduler.add_job(id='Schedule Task', func= schedulerTask, trigger = 'cron', hour = '*', minute = '00,10,20,30,40,55')
    scheduler.start()

    app.run(debug=False, host='0.0.0.0', port=int(port))
