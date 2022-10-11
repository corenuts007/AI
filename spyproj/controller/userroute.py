from flask import render_template, Response, request
from spyproj import app
# from flask_pymongo import PyMongo
from spyproj.repository.userdetails_repository import UserDetails
from spyproj.model.user_details_data import UserDetailsData
from flask import jsonify
import json
from bson import json_util


@app.route('/')
def home():
    return "Hello"


@app.route('/users', methods=['GET'])
def users():
    try:
        # find method returns cursor object
        usercursor = UserDetails.get_users()
        if usercursor:
            print("*********")
            # convert cursor to list of dictionaries
            userlist = list(usercursor)
            print("**aaa***abcd*", userlist)
            users = []
            password = None
            for user in userlist:
                id = user['_id']
                username = user['username']
                # if password is None:
                password = user['password']
                dataDict = {
                    'id': str(id),
                    'username': username,
                    'password': password
                }
                users.append(dataDict)
            # convert into json
            # json_data = json.dumps(xyz, default = str)
            json_data = jsonify(users)
            print("---------", str(json_data))
            # return Response(response="suceess", status=200, mimetype="application/json")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*", ex)
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/userByName', methods=['GET'])
def userByName():
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
        data = UserDetailsData.user_data(request)
        print("data :", data)
        # userdata = {'username':request.json["username"], 'password':request.json["password"]}
        # print(userdata)
        UserDetails.create_user(data)
        return Response(response="User created successfully", status=200, mimetype="application/json")
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


if __name__ == '__main__':
    app.run()
