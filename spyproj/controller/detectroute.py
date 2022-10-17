from flask import render_template, Response, request
from spyproj import app
from spyproj.service.detect_service import Detect_Service
from flask import jsonify



@app.route('/detective',  methods=['GET'])
def detective():
    print('helllo')
    Detect_Service()
    return 'hello'


