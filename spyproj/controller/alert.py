from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.alertdetails_repository import AlertDetails
from spyproj.model.alert_details_data import AlertDetailsData
from flask import jsonify
from loguru import logger

@app.route('/alerts', methods=['GET'])
def alerts():
    logger.debug("In Alert.py - alerts - start")
    try:
        # find method returns cursor object
        alertcursor = AlertDetails.get_alerts()
        if alertcursor:
            # convert cursor to list of dictionaries
            alertlist = list(alertcursor)
            alerts = []

            for alert in alertlist:
                org_name = ''
                camera_name = ''
                camera_location = ''
                alert_time = ''
                video_locaion = ''
                id = alert['_id']
                # if alertlocation is None:
                if 'org_name' in alert:
                    org_name = alert['org_name']

                if 'camera_name' in alert:
                    camera_name = alert['camera_name']

                if 'camera_location' in alert:
                    camera_location = alert['camera_location']

                if 'alert_time' in alert:
                    alert_time = alert['alert_time']
                if 'video_locaion' in alert:
                    video_locaion = alert['video_locaion']
                dataDict = {
                    'id': str(id),
                    'org_name': org_name,
                    'camera_name': camera_name,
                    'camera_location': camera_location,
                    'alert_time': alert_time,
                    'video_locaion': video_locaion
                }
                alerts.append(dataDict)
            # convert into json
            # json_data = json.dumps(xyz, default = str)
            json_data = jsonify(alerts)
            # return Response(response="suceess", status=200, mimetype="application/json")
            logger.debug("In Alert.py - alerts - end")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*", ex)
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")



@app.route('/createalert', methods=['GET', 'POST'])
def createalert():
    try:
        print('hi')
        newDataReq = request.json["newData"]

        data = AlertDetailsData.alert_data(request)
        print("data :", data)
        AlertDetails.create_alert(data)
        return Response(response="Alert created successfully", status=200, mimetype="application/json")
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")



if __name__ == '__main__':
    app.run()
