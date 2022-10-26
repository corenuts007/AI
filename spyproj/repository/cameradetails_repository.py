from spyproj.repository.connection import Connection


class CameraDetails:
    def get_cameras():
        db_conn = Connection.get_database()
        cameradatalist = db_conn.get_collection('Camera_Details').find()
        return cameradatalist

    def get_camerabyid(strx):
        db_conn = Connection.get_database()
        cameradatalist = db_conn.get_collection('Camera_Details').find(strx)
        return cameradatalist

    def create_camera(data):
        db_conn = Connection.get_database()
        print("inside")
        db_conn.get_collection('Camera_Details').insert_one(data)
        print("ousdie")

    def update_camera(filter, updatedData):
        db_conn = Connection.get_database()
        print("inside - update")
        db_conn.get_collection('Camera_Details').update_one(
            filter, updatedData)
        print("ousdie - update")

    def delete_camera(filter):
        db_conn = Connection.get_database()
        print("inside - delete")
        db_conn.get_collection('Camera_Details').delete_one(filter)
        print("ousdie - delete")
    
    def get_camera_details_bystatus(status):
        db_conn = Connection.get_database()
        cameradatalist = db_conn.get_collection('Camera_Details').find(status)
        return cameradatalist
    
    def find_camera_details_by_params(filter):
        db_conn = Connection.get_database()
        cameradatalist = db_conn.get_collection('Camera_Details').find(filter)
        return cameradatalist
