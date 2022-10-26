from tokenize import group


class CameraHistoryData:
   
    def __init__(self, group_name, building_name, cam_name, starttime, endtime):
        self.group_name = group_name
        self.building_name = building_name
        self.cam_name = cam_name
        self.starttime = starttime
        self.endtime = endtime

    def camera_history_data(data):
 
        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        if(data.group_name is not None):
            finalvalue['group_name'] = data.group_name
        if(data.building_name is not  None):
            finalvalue['building_name'] = data.building_name
        if(data.cam_name is not None):
            finalvalue['cam_name'] = data.cam_name
        if(data.starttime is not None):
            finalvalue['starttime'] = data.starttime
        if(data.endtime is not None):
            finalvalue['endtime'] = data.endtime

        print(finalvalue)
        return finalvalue

    def populate_filter(group_name, building_name, cam_name):
 
        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        finalvalue['group_name'] = group_name
        finalvalue['building_name'] = building_name
        finalvalue['cam_name'] = cam_name
        print(finalvalue)
        return finalvalue


    def update_camera_history_data(self, request):
        updatedata = request.json["updateData"]

        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        finalvalue = self.__camera_history_data(updatedata)
        print(finalvalue)
        return finalvalue

    def __camera_history_data(self,data):
        finalvalue = {}
        # NEW Fields AFTER confirmatin
        if ("group_name" in data):
            finalvalue['group_name'] = data["group_name"]

        if ("building_name" in data):
            finalvalue['building_name'] = data["building_name"]

        if ("cam_name" in data):
            finalvalue['cam_name'] = data["cam_name"]

        # if ("url_or_ip_address" in data):
        #     finalvalue['url_or_ip_address'] = data["url_or_ip_address"]
    
        if ("starttime" in data):
            finalvalue['starttime'] = data["starttime"]
        
        if ("endtime" in data):
            finalvalue['endtime'] = data["endtime"]
        
        print(finalvalue)
        return finalvalue
