class CameraDetailsData:
    def camera_data(self, request):
        newdata = request.json["newData"]

        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}

        # NEW Fields AFTER confirmatin
        finalvalue = self.__camera_data(newdata)
        
        print(finalvalue)
        return finalvalue

    def camera_updateData(self, request):
        updatedata = request.json["updateData"]

        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        finalvalue = self.__camera_data(updatedata)
        print(finalvalue)
        return finalvalue

    def __camera_data(self,data):
        finalvalue = {}
        # NEW Fields AFTER confirmatin
        if ("group_name" in data):
            finalvalue['group_name'] = data["group_name"]

        if ("building_name" in data):
            finalvalue['building_name'] = data["building_name"]

        if ("cam_name" in data):
            finalvalue['cam_name'] = data["cam_name"]

        if ("url_or_ip_address" in data):
            finalvalue['url_or_ip_address'] = data["url_or_ip_address"]
    
        if ("run_status" in data):
            finalvalue['run_status'] = data["run_status"]

        if ("phone_numbers" in data):
            finalvalue['phone_numbers'] = data["phone_numbers"]
        
        if ("email_address" in data):
            finalvalue['email_address'] = data["email_address"]
        
        if ("monday_starttime" in data):
            finalvalue['monday_starttime'] = data["monday_starttime"]
        
        if ("monday_nextday_endtime" in data):
            finalvalue['monday_nextday_endtime'] = data["monday_nextday_endtime"]
        
        if ("tuesday_starttime" in data):
            finalvalue['tuesday_starttime'] = data["tuesday_starttime"]
        
        if ("tuesday_nextday_endtime" in data):
            finalvalue['tuesday_nextday_endtime'] = data["tuesday_nextday_endtime"]
        
        if ("wednesday_starttime" in data):
            finalvalue['wednesday_starttime'] = data["wednesday_starttime"]
        
        if ("wednesday_nextday_endtime" in data):
            finalvalue['wednesday_nextday_endtime'] = data["wednesday_nextday_endtime"]
        
        if ("thursday_starttime" in data):
            finalvalue['thursday_starttime'] = data["thursday_starttime"]
        
        if ("thursday_nextday_endtime" in data):
            finalvalue['thursday_nextday_endtime'] = data["thursday_nextday_endtime"]

        if ("friday_starttime" in data):
            finalvalue['friday_starttime'] = data["friday_starttime"]
        
        if ("friday_nextday_endtime" in data):
            finalvalue['friday_nextday_endtime'] = data["friday_nextday_endtime"]

        if ("saturday_starttime" in data):
            finalvalue['saturday_starttime'] = data["saturday_starttime"]
        
        if ("saturday_nextday_endtime" in data):
            finalvalue['saturday_nextday_endtime'] = data["saturday_nextday_endtime"]

        if ("sunday_starttime" in data):
            finalvalue['sunday_starttime'] = data["sunday_starttime"]
        
        if ("sunday_nextday_endtime" in data):
            finalvalue['sunday_nextday_endtime'] = data["sunday_nextday_endtime"]
        
        print(finalvalue)
        return finalvalue

    def populate_filter(group_name, building_name, cam_name, status):
 
        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        finalvalue['group_name'] = group_name
        finalvalue['building_name'] = building_name
        if cam_name != '':
            finalvalue['cam_name'] = cam_name
        if status != '':
            finalvalue['run_status'] = status
        print(finalvalue)
        return finalvalue

