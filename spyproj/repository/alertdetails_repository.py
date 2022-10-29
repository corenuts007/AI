from spyproj.repository.connection import Connection


class AlertDetails:
    def get_alerts():
        db_conn = Connection.get_database()
        alertdatalist = db_conn.get_collection('Alert_Details').find()
        return alertdatalist

    def get_alertbyid(strx):
        db_conn = Connection.get_database()
        alertdatalist = db_conn.get_collection('Alert_Details').find(strx)
        return alertdatalist

    def create_alert(data):
        db_conn = Connection.get_database()
        print("inside")
        db_conn.get_collection('Alert_Details').insert_one(data)
        print("ousdie")

    def update_alert(filter, updatedData):
        db_conn = Connection.get_database()
        print("inside - update")
        db_conn.get_collection('Alert_Details').update_one(
            filter, updatedData)
        print("ousdie - update")

    def delete_alert(filter):
        db_conn = Connection.get_database()
        print("inside - delete")
        db_conn.get_collection('Alert_Details').delete_one(filter)
        print("ousdie - delete")
    
    def find_alert_details_by_filterCondition(filter):
        db_conn = Connection.get_database()
        alertdatalist = db_conn.get_collection('Alert_Details').find(filter)
        return alertdatalist
