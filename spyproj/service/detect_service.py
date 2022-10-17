from spyproj.yolov7.detect_objects import Detective

class Detect_Service:
    def __init__(self):
        print('detect service constructor')
        d = Detective()
        print('DETCTIVE')
        d.detect_object_method()

