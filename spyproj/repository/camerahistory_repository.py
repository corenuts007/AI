from spyproj.repository.connection import Connection


class CameraHistory:
    def get_camera_history():
        db_conn = Connection.get_database()
        cameradatalist = db_conn.get_collection('Camera_History').find()
        return cameradatalist

    def create_camera_history(data):
        db_conn = Connection.get_database()
        print("inside")
        db_conn.get_collection('Camera_History').insert_one(data)
        print("ousdie")

    def update_camera_history(filter, updatedData):
        db_conn = Connection.get_database()
        print("inside - update")
        db_conn.get_collection('Camera_History').update_one(
            filter, updatedData)
        print("ousdie - update")

    def delete_camera_history(filter):
        db_conn = Connection.get_database()
        print("inside - delete")
        db_conn.get_collection('Camera_History').delete_one(filter)
        print("ousdie - delete")
    
    def find_camera_history_by_params(filter):
        db_conn = Connection.get_database()
        cameradatalist = db_conn.get_collection('Camera_History').find(filter)
        return cameradatalist

