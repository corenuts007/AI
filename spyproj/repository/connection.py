from pymongo import MongoClient


class Connection:

    def get_database():
        client = MongoClient(
            "mongodb+srv://spyproject:kamala@cluster0.5kaedwv.mongodb.net/test?retryWrites=true&w=majority")
        db = client.get_database('Spy_Project')
        return db
