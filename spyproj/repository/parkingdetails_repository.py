from spyproj.repository.connection import Connection


class ParkingDetails:
    def createVehicleDetails(data):
        db_conn = Connection.get_database()
        print("inside")
        db_conn.get_collection('Parking_Details').insert_one(data)
        print("ousdie")

    def updateVehicleDetails(filter, updatedData):
        db_conn = Connection.get_database()
        print("inside - update")
        db_conn.get_collection('Parking_Details').update_one(
            filter, updatedData)
        print("ousdie - update")

    def findPartkingDetailsByFilterCondition(filter):
        db_conn = Connection.get_database()
        parkingDataList = db_conn.get_collection('Parking_Details').find(filter)
        return parkingDataList
