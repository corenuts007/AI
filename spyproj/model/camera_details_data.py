class CameraDetailsData:
    def camera_data(request):
        newdata = request.json["newData"]

        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        if ("cameraname" in newdata):
            cameraname = newdata["cameraname"]
            finalvalue['cameraname'] = cameraname

        if ("cameralocation" in newdata):
            cameralocation = newdata["cameralocation"]
            finalvalue['cameralocation'] = cameralocation

        if ("url" in newdata):
            url = newdata["url"]
            finalvalue['url'] = url

        if ("monday_AlertStartTime" in newdata):
            monday_AlertStartTime = newdata["monday_AlertStartTime"]
            finalvalue['monday_AlertStartTime'] = monday_AlertStartTime

        if ("monday_AlertEndTime" in newdata):
            monday_AlertEndTime = newdata["monday_AlertEndTime"]
            finalvalue['monday_AlertEndTime'] = monday_AlertEndTime

        print(finalvalue)
        return finalvalue

    def camera_UpdateData(request):
        newdata = request.json["updateData"]

        # finalvalue = {'cameraname':cameraname, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        if ("cameraname" in newdata):
            cameraname = newdata["cameraname"]
            finalvalue['cameraname'] = cameraname

        if ("cameralocation" in newdata):
            cameralocation = newdata["cameralocation"]
            finalvalue['cameralocation'] = cameralocation

        if ("url" in newdata):
            url = newdata["url"]
            finalvalue['url'] = url

        if ("monday_AlertStartTime" in newdata):
            monday_AlertStartTime = newdata["monday_AlertStartTime"]
            finalvalue['monday_AlertStartTime'] = monday_AlertStartTime

        if ("monday_AlertEndTime" in newdata):
            monday_AlertEndTime = newdata["monday_AlertEndTime"]
            finalvalue['monday_AlertEndTime'] = monday_AlertEndTime

        print(finalvalue)
        return finalvalue
