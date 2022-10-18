class AlertDetailsData:
    def alert_data(request):
        newdata = request.json["newData"]

        # finalvalue = {'alertname':alertname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        if ("alert_name" in newdata):
            alert_name = newdata["alert_name"]
            finalvalue['alert_name'] = alert_name
        
        if ("org_name" in newdata):
            org_name = newdata["org_name"]
            finalvalue['org_name'] = org_name

        if ("camera_name" in newdata):
            camera_name = newdata["camera_name"]
            finalvalue['camera_name'] = camera_name

        if ("camera_location" in newdata):
            camera_location = newdata["camera_location"]
            finalvalue['camera_location'] = camera_location

        if ("alert_time" in newdata):
            alert_time = newdata["alert_time"]
            finalvalue['alert_time'] = alert_time

        if ("video_locaion" in newdata):
            video_locaion = newdata["video_locaion"]
            finalvalue['video_locaion'] = video_locaion

        print(finalvalue)
        return finalvalue
