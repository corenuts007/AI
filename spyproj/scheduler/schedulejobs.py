from spyproj.service.detect_service import Detect_Service
from flask import jsonify
class Schedule_jobs:

    def scheduler_tasks():
        print('welcome schedulerTasks')
        detect = Detect_Service()
        detect.run_detect_process()
        return
