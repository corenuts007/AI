from flask import render_template, Response
from spyproj import app
from spyproj.repository.history_repository import History
from flask import jsonify
import json


@app.route('/histories')
@app.route('/histories', methods=['GET'])
def histories():
    try:
        # find method returns cursor object
        historycursor = History.get_histories()
        if historycursor:
            print("*****")
            # convert cursor to list of dictionaries
            historylist = list(historycursor)
            histories = []
            for history in historylist:
                history.pop('_id')
                histories.append(str(history))
                print(history)

            print("---------")
            # convert into json
            #json_data = json.dumps(xyz, default = str)
            json_data = jsonify(histories)
            # return Response(response="suceess", status=200, mimetype="application/json")
            return json_data
        else:
            return "Hello No Data"
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


@app.route('/createhistory', methods=['GET', 'POST'])
def createhistory():
    try:
        historydata = History.create_history()
        return Response(response="History created successfully", status=200, mimetype="application/json")
    except Exception as ex:
        print("*Exception*")
        print(ex.__str__())
        return Response(response="Failure", status=500, mimetype="application/json")


if __name__ == '__main__':
    app.run()
