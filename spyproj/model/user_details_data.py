class UserDetailsData:
    def user_data(request):
        newdata = request.json["newData"]
        username = newdata["username"]
        password = newdata["password"]
        finalvalue = {}
        # finalvalue = {'username':username, 'password':password}
        # the above statement treat as String... but we should pass as dict.. so follow the below conversion before inserting record in DB
        finalvalue['username'] = username
        finalvalue['password'] = password
        print(finalvalue)
        return finalvalue
