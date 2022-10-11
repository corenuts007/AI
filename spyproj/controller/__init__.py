from flask import Flask

app = Flask(__name__)

from spyproj.controller import userroute
from spyproj.controller import historyroute
