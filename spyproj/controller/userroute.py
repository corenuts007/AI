from flask import render_template, Response, request
from spyproj import app
# from flask_pymongo import PyMongo
from spyproj.repository.userdetails_repository import UserDetails
from spyproj.model.user_details_data import UserDetailsData
from flask import jsonify



@app.route('/')
def home():
    return "Hello"


@app.route('/users', methods=['GET'])
def users():
    try:
        # find method returns cursor object
        usercursor = UserDetails.get_users()
        if usercursor:
            # convert cursor to list of dictionaries
            userlist = list(usercursor)
            users = []

            for user in userlist:
                password = ''
                location = ''
                id = user['_id']
                username = user['username']
                # if password is None:
                if 'password' in user:
                    password = user['password']

                if 'location' in user:
                    location = user['location']

                dataDict = {
                    'id': str(id),
                    'username': username,
                    'password': password,
                    'location': location
                }
                users.append(dataDict)
            # convert into json
            # json_data = json.dumps(xyz, default = str)
            json_data = jsonify(users)

            # return Response(response="suceess", status=200, mimetype="application/json")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*", ex)
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/userByName', methods=['GET'])
def getUserByName():
    try:

        # Request from front end as json object
        # {"username":"Raja"} in postman
        print(request.json["username"])
        # find method returns cursor object
        usercursor = UserDetails.get_userbyid(
            {'username': request.json["username"]})
        if usercursor:
            print("***   *")
            # convert cursor to list of dictionaries
            userlist = list(usercursor)
            users = []
            for user in userlist:
                user.pop('_id')
                users.append(str(user))
                print(user)

            print("---------")
            # convert into json
            # json_data = json.dumps(xyz, default = str)
            json_data = jsonify(users)
            # return Response(response="suceess", status=200, mimetype="application/json")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
    try:
        print('hi')
        newDataReq = request.json["newData"]

        # pass the primary key as filter in order to update document based on it
        usercursor = UserDetails.get_userbyid(
            {'username': newDataReq["username"]})

        # if already user is exist then skip the create user
        userlist = list(usercursor)
        if len(userlist) != 0:
            return Response(response="User already exist, please try again", status=200, mimetype="application/json")

        # if user not exist then create it
        data = UserDetailsData.user_data(request)
        print("data :", data)
        UserDetails.create_user(data)
        return Response(response="User created successfully", status=200, mimetype="application/json")
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/updateUserByName', methods=['GET', 'POST'])
def updateUserByName():
    try:
        print("****==>", request.json["updateData"])
        updateDataReq = request.json["updateData"]

        # pass the primary key as filter in order to update document based on it
        usercursor = UserDetails.get_userbyid(
            {'username': updateDataReq["username"]})

        # if  user is not exist then skip the update user
        userlist = list(usercursor)
        if len(userlist) == 0:
            return Response(response="User not exist, please try again", status=200, mimetype="application/json")

        # pass the primary key as filter in order to update document based on it
        filter = {'username': updateDataReq["username"]}
        print("====filter====>", filter)

        # set what are the values need to update in document
        dataForUpdate = UserDetailsData.user_UpdateData(request)
        print("data :", dataForUpdate)
        updatedData = {"$set": dataForUpdate}
        UserDetails.update_user(filter, updatedData)

        print("*** After Update  *")
        return Response(response="Updated suceessfully", status=200, mimetype="application/json")

    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Update is Failed", status=500, mimetype="application/json")


@app.route('/deleteUserByName', methods=['GET', 'POST'])
def deleteUserByName():
    try:

        print(request.json["username"])
        # find method returns cursor object
        usercursor = UserDetails.get_userbyid(
            {'username': request.json["username"]})

        # if  user is not exist then skip the delete user
        userlist = list(usercursor)
        if len(userlist) == 0:
            return Response(response="User not exist, please try again", status=200, mimetype="application/json")

        # pass the primary key data as filter to delete the document
        filter = {'username': request.json["username"]}
        print(filter)
        UserDetails.delete_user(filter)

        print("*** After Delete  *")
        return Response(response="Deleted suceessfully", status=200, mimetype="application/json")

    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Delete is Failed", status=500, mimetype="application/json")


if __name__ == '__main__':
    app.run()
