from datetime import datetime

class ParkingDetailsData:
    def getVehicleDetails(request):
        
        # finalvalue = {'alertname':alertname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}

        finalvalue['vechileNumber'] = request.form.get('vechileNumber')
        finalvalue['org_name'] = request.form.get("org_name")
        finalvalue['in_time'] = datetime.now()
        finalvalue['out_time'] = ''
        finalvalue['status'] = request.form.get("status")
        finalvalue['amtTobePaid'] =''
        finalvalue['total_hours']=''
       
        return finalvalue

    def getVehicleUpdateData(request):
        #updatedata = request.json["updateData"]

        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        finalvalue['vechileNumber'] = request.form.get('vechileNumber')
        finalvalue['org_name'] = request.form.get("org_name")
        finalvalue['out_time'] = datetime.now()
        finalvalue['status'] = request.form.get("status")
       
        return finalvalue

    def __vechile_data(self,newdata):
        finalvalue = {}
        # NEW Fields AFTER confirmatin
        if ("vechileNumber" in newdata):
            vechileNumber = newdata["vechileNumber"]
            finalvalue['vechileNumber'] = vechileNumber
        
        if ("org_name" in newdata):
            org_name = newdata["org_name"]
            finalvalue['org_name'] = org_name
        
        if ("in_time" in newdata):
            in_time = newdata["in_time"]
            finalvalue['in_time'] = in_time

        if ("out_time" in newdata):
            out_time = newdata["out_time"]
            finalvalue['out_time'] = out_time
        
        
        if ("status" in newdata):
            status = newdata["status"]
            finalvalue['status'] = status




        
        print(finalvalue)
        return finalvalue

