from spyproj.repository.connection import Connection

class History:
    def get_histories():
        db_conn = Connection.get_database()
        userdatalist = db_conn.get_collection('History').find()
        return userdatalist
    
    def create_history():
        db_conn = Connection.get_database()
        print("inside")
        db_conn.get_collection('History').insert_one({'username':'Raja', 'address':'Blr'})
        print("ousdie")
