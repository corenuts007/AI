import os
from spyproj import app

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=int(port))
