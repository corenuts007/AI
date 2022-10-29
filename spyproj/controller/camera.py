from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.cameradetails_repository import CameraDetails
from spyproj.model.camera_details_data import CameraDetailsData
from flask import jsonify

@app.route('/cameras', methods=['GET'])
def cameras():
    try:
        # find method returns cursor object
        cameracursor = CameraDetails.get_cameras()
        if cameracursor:
            # convert cursor to list of dictionaries
            cameralist = list(cameracursor)
            cameras = []

            for camera in cameralist:
                cameralocation = ''
                url = ''
                monday_AlertStartTime = ''
                monday_AlertEndTime = ''
                id = camera['_id']
                cameraname = camera['cameraname']
                # if cameralocation is None:
                if 'cameralocation' in camera:
                    cameralocation = camera['cameralocation']

                if 'url' in camera:
                    url = camera['url']

                if 'monday_AlertStartTime' in camera:
                    monday_AlertStartTime = camera['monday_AlertStartTime']

                if 'monday_AlertEndTime' in camera:
                    monday_AlertEndTime = camera['monday_AlertEndTime']

                dataDict = {
                    'id': str(id),
                    'url': url,
                    'monday_AlertStartTime': monday_AlertStartTime,
                    'monday_AlertEndTime': monday_AlertEndTime,
                    'cameralocation': cameralocation,
                    'cameraname': cameraname
                }
                cameras.append(dataDict)
            # convert into json
            # json_data = json.dumps(xyz, default = str)
            json_data = jsonify(cameras)
            print("search==", cameras)
            # return Response(response="suceess", status=200, mimetype="application/json")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*", ex)
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/cameraByName', methods=['GET'])
def getCameraByName():
    try:

        # Request from front end as json object
        # {"cameraname":"Raja"} in postman
        print(request.json["cameraname"])
        # find method returns cursor object
        cameracursor = CameraDetails.get_camerabyid(
            {'cameraname': request.json["cameraname"]})
        if cameracursor:
            print("***   *")
            # convert cursor to list of dictionaries
            cameralist = list(cameracursor)
            cameras = []
            for camera in cameralist:
                camera.pop('_id')
                cameras.append(str(camera))
                print(camera)

            print("---------")
            # convert into json
            # json_data = json.dumps(xyz, default = str)
            json_data = jsonify(cameras)
            # return Response(response="suceess", status=200, mimetype="application/json")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/createcamera', methods=['GET', 'POST'])
def createcamera():
    try:
        print('hi')
        newDataReq = request.json["newData"]

        # pass the primary key as filter in order to update document based on it
        cameracursor = CameraDetails.get_camerabyid(
            {'cameraname': newDataReq["cameraname"]})

        # if already camera is exist then skip the create camera
        cameralist = list(cameracursor)
        if len(cameralist) != 0:
            return Response(response="Camera already exist, please try again", status=200, mimetype="application/json")

        # if camera not exist then create it
        data = CameraDetailsData.camera_data(request)
        print("data :", data)
        CameraDetails.create_camera(data)
        return Response(response="Camera created successfully", status=200, mimetype="application/json")
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/updateCameraByName', methods=['GET', 'POST'])
def updateCameraByName():
    try:
        print("****==>", request.json["updateData"])
        updateDataReq = request.json["updateData"]

        # pass the primary key as filter in order to update document based on it
        cameracursor = CameraDetails.get_camerabyid(
            {'cameraname': updateDataReq["cameraname"]})

        # if  camera is not exist then skip the update camera
        cameralist = list(cameracursor)
        if len(cameralist) == 0:
            return Response(response="Camera not exist, please try again", status=200, mimetype="application/json")

        # pass the primary key as filter in order to update document based on it
        filter = {'cameraname': updateDataReq["cameraname"]}
        print("====filter====>", filter)

        # set what are the values need to update in document
        dataForUpdate = CameraDetailsData.camera_updateData(request)
        print("data :", dataForUpdate)
        updatedData = {"$set": dataForUpdate}
        CameraDetails.update_camera(filter, updatedData)

        print("*** After Update  *")
        return Response(response="Updated suceessfully", status=200, mimetype="application/json")

    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Update is Failed", status=500, mimetype="application/json")


@app.route('/deleteCameraByName', methods=['GET', 'POST'])
def deleteCameraByName():
    try:

        print(request.json["cameraname"])
        # find method returns cursor object
        cameracursor = CameraDetails.get_camerabyid(
            {'cameraname': request.json["cameraname"]})

        # if  camera is not exist then skip the delete camera
        cameralist = list(cameracursor)
        if len(cameralist) == 0:
            return Response(response="Camera not exist, please try again", status=200, mimetype="application/json")

        # pass the primary key data as filter to delete the document
        filter = {'cameraname': request.json["cameraname"]}
        print(filter)
        CameraDetails.delete_camera(filter)

        print("*** After Delete  *")
        return Response(response="Deleted suceessfully", status=200, mimetype="application/json")

    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Delete is Failed", status=500, mimetype="application/json")


if __name__ == '__main__':
    app.run()
