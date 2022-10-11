from spyproj.repository.connection import Connection

class UserDetails:
    def get_users():
        db_conn = Connection.get_database()
        userdatalist = db_conn.get_collection('User_Details').find()
        return userdatalist
    
    def get_userbyid(strx):
        db_conn = Connection.get_database()
        userdatalist = db_conn.get_collection('User_Details').find(strx)
        return userdatalist
    
    def create_user(data):
        db_conn = Connection.get_database()
        print("inside")
        db_conn.get_collection('User_Details').insert_one(data)
        print("ousdie")
