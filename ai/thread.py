from threading import Thread, Lock
import time
import thread
import cv2

# Device data and its mutex
devs = []
d_mtx = Lock()


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Device:
    id = 0
    cams = []

    def __init__(self, id, cams):
        self.id = id
        self.cams = cams


class Camera:
    id = 0
    areas = []

    def __init__(self, id, areas):
        self.id = id
        self.areas = areas


class DetectionArea:
    id = 0
    img = None
    occuppied = False

    def __init__(self, id, img, occuppied):
        self.id = id
        self.img = img
        self.occuppied = occuppied


def pull_warnings():
    return ""


def occupancy_list(dev_id, cam_id):
    d_mtx.acquire()
    
    arr = [] # (id, occupancy_state)
    for dev in devs:
        if dev.id == dev_id:
            for cam in dev.cams:
                if cam.id == cam_id:
                    arr.append(area.id, area.occuppied)

    d_mtx.release()
    return arr


def update_frame(img, dev_id, cam_id, rects):
    d_mtx.acquire()
    
    # Check if device and camera of this id exists
    camera = None
    for dev in devs:
        if dev.id == dev_id:
            for cam in dev.cams:
                if cam.id == cam_id:
                    camera = cam

    # If no device of those ids were detected or the rects are incorrect stop execution
    if camera == None or len(camera.areas) != len(rects):
        return

    # Load in the crops for the camera and reset occupancy for this 
    for i in range(0, len(rects)):
        camera.areas[i].img = img[rects[i].y : rects[i].y+rects[i].h,
            rects[i].x : rects[i].x+rects[i].w]
        camera.areas[i].occuppied = False

    d_mtx.release()


def add_dev(device):
    d_mtx.acquire()
    devs.append(device)
    d_mtx.release()


def ai_thread_start(devices=None):
    
    if devices == None:
        print("No devices passed to the AI thread. Starting empty-handed")
    else:
        devs = devices

    # TODO: Create/Import a model
    model = None
    
    while True:
        time.Sleep(0.2) # sleep for 0.2 sec
        
        if len(devs) == 0:
            continue

        # Detect for each area
        d_mtx.acquire()
        for dev in devs:
            for cam in dev.cams:
                for area in cam.areas:
                    area.occuppied = model.Detect(area.img)
        d_mtx.release()

    pass
