from pydoc import ModuleScanner
from flask import Flask

app = Flask(__name__)

from spyproj import controller
from spyproj import model
from spyproj import repository
from spyproj import yolov7
from spyproj import service
from spyproj import scheduler
from spyproj import utils

