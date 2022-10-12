class UserDetailsData:
    def user_data(request):
        newdata = request.json["newData"]

        # finalvalue = {'username':username, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        if ("username" in newdata):
            username = newdata["username"]
            finalvalue['username'] = username

        if ("password" in newdata):
            password = newdata["password"]
            finalvalue['password'] = password

        if ("location" in newdata):
            location = newdata["location"]
            finalvalue['location'] = location
       
        print(finalvalue)
        return finalvalue
    
    def user_UpdateData(request):
        newdata = request.json["updateData"]

        # finalvalue = {'username':username, 'password':password}
        # the above statement treat as String... but we should pass as dict..
        # so follow the below conversion before inserting record in DB

        finalvalue = {}
        if ("username" in newdata):
            username = newdata["username"]
            finalvalue['username'] = username

        if ("password" in newdata):
            password = newdata["password"]
            finalvalue['password'] = password

        if ("location" in newdata):
            location = newdata["location"]
            finalvalue['location'] = location
       
        print(finalvalue)
        return finalvalue
