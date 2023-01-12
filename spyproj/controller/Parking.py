import math
from flask import render_template, Response, request
from spyproj import app
from spyproj.repository.parkingdetails_repository import ParkingDetails

from spyproj.model.parking_details_data import ParkingDetailsData
from flask import jsonify
from loguru import logger
from datetime import datetime




@app.route('/createVehicleDetails', methods=['GET', 'POST'])
def createVehicleDetails():
    try:
       #newDataReq = request.json["newData"]
        
        print("createVehicleDetails==>",request.get_data())
        data = ParkingDetailsData.getVehicleDetails(request)
        print("data :", data)
        ParkingDetails.createVehicleDetails(data)
        return Response(response="Parking Intime Info created successfully", status=200, mimetype="application/json")
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/updateVehicleDetails', methods=['GET', 'POST'])
def updateVehicleDetails():
    try:
        #print("updateVehicleDetails==>",request.get_data())
        updateDataReq = ParkingDetailsData.getVehicleDetails(request)
         

        filter =  {'vechileNumber': updateDataReq["vechileNumber"]}
        # pass the primary key as filter in order to update document based on it
        print("====filter====>", filter)
        # pass the primary key as filter in order to update document based on it
        vechicleCursor = ParkingDetails.findPartkingDetailsByFilterCondition(filter)
        
        if (len(list(vechicleCursor))) <= 0 :
            print("No Vechile found", (len(list(vechicleCursor))))
            exceptionInfo = {}
            exceptionInfo['errorMsg'] = 'vechile Number not exist, please Check the Vechile No'
            json_error_data = jsonify(exceptionInfo)

            return json_error_data
 
        print("====1 vechicle identified ====>")
     
        intime=datetime.now()
        for vechicle in vechicleCursor:
            intime = vechicle['in_time']
            print('intime in looopp******* ==>',intime)

        
        # set what are the values need to update in document
        dataForUpdate = ParkingDetailsData.getVehicleUpdateData(request)
        #print("data 11:", dataForUpdate)
        
        
        outtime = dataForUpdate.get('out_time')
        print('out_time ==>',outtime)
        
        buffermins=10
        amtperHour=20
        

        hours =0
        #start_time = datetime.strptime(intime, "%H:%M:%S")
        #end_time = datetime.strptime(outtime, "%H:%M:%S")
        delta = outtime - intime
        total_seconds = delta.total_seconds()
        print('Time total_seconds==>',total_seconds)
        total_mins = total_seconds//60
        print('Time total_mins==>',total_mins)
        if(total_mins<=59):
            hours = 1
            print('less than a hour*************')
        else :
            total_hours = total_mins//60
            remainingMins = total_mins%60
            print('total_hours 11==>',total_hours)
            print('remainingMins 111=>',remainingMins)
            if remainingMins>=buffermins:
                hours= total_hours+1
            else:
                hours=total_hours

        

        amtTobePaid = math.floor(amtperHour*hours)

        dataForUpdate['amtTobePaid'] =amtTobePaid
        dataForUpdate['total_hours']=hours
        
        print('calculated  hoursss$$$$$$$$$*************', hours)
        print('amtTobePaid$$$$$$$$$*************', amtTobePaid)

        updatedData = {"$set": dataForUpdate}
        ParkingDetails.updateVehicleDetails(filter, updatedData)
        dataForUpdate['in_time']=intime
        
        json_data = jsonify(dataForUpdate)

        #print("*** After Update  *",str(json_data))
        return json_data

    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Update is Failed", status=500, mimetype="application/json")



if __name__ == '__main__':
    app.run()
