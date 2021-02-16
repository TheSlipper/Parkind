from threading import Thread, Lock
import copy
import time
import cv2
from ai.net import *

# Device data and its mutex
devs = []
d_mtx = Lock()
stop = False

# Thread started
th_started = False
th = None


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
    occuppied = False
    rect = None

    def __init__(self, id, occuppied, rect):
        self.id = id
        self.occuppied = occuppied
        self.rect = rect


def stop_exec():
    global d_mtx
    global stop
    d_mtx.acquire()
    stop = True
    d_mtx.release()


def pull_warnings():
    return ""


def occupancy_list(dev_id, cam_id):
    d_mtx.acquire()
    
    arr = [] # (id, occupancy_state)
    for dev in devs:
        if dev.id == dev_id:
            for cam in dev.cams:
                if cam.id == cam_id:
                    arr.append((area.id, area.occuppied))

    d_mtx.release()
    return arr


def update_frame(img, dev_id, cam_id):
    global d_mtx
    global devs
    global th_started
    d_mtx.acquire()
    
    # Get the camera
    camera = None
    for i in range(0, len(devs)):
        if devs[i].id == dev_id:
            for j in range(0, len(devs[i].cams)):
                if devs[i].cams[j].id == cam_id:
                    camera = devs[i].cams[j]
                    break
    
    # If no device of those ids were detected or the rects are incorrect stop execution
    if camera == None:
        return False

    # Load in the crops for the camera and reset occupancy for this
    for i in range(0, len(camera.areas)):
        rect = camera.areas[i].rect
        c_img = img[rect.y : rect.y+rect.h, rect.x : rect.x+rects[i].w]
        f_name = str(dev_id) + "_" + str(cam_id) + "_" + str(camera.areas[i].id) + ".jpg"
        cv2.imwrite("static/img/recordings/crops/" + f_name, c_img)

    d_mtx.release()
    return True


def started():
    global th_started
    return th_started


def add_dev(device):
    d_mtx.acquire()
    devs.append(device)
    d_mtx.release()


def ai_thread_start(model_path = None, devices=None):
    global devs
    global th_started
    global d_mtx

    if devices == None:
        print("No devices passed to the AI thread. Starting empty-handed")
    else:
        devs = copy.deepcopy(devices)

    # TODO: Create/Import a model
    model = import_model(model_path)
    print("Successfully loaded a model")

    # Log how many entities registered
    dev_cnt = len(devs)
    cams_cnt = 0
    areas_cnt = 0
    for dev in devs:
        for cam in dev.cams:
            cams_cnt += 1
            for area in cam.areas:
                areas_cnt += 1
    
    print("AI Module registered: ", dev_cnt, " devices, ", cams_cnt, " cameras and ", areas_cnt, " areas.")
    print("AI Module is up and running...")

    # TODO: Time it correctly so that each run actually lasts a second
    while True:
        time.sleep(0.2) # sleep for 0.2 sec
        
        if len(devs) == 0:
            continue

        if stop:
            d_mtx.acquire()
            devs = []
            th_started = False
            d_mtx = Lock()
            return

        # Detect for each area
        d_mtx.acquire()
        for dev in devs:
            for cam in dev.cams:
                for area in cam.areas:
                    f_name = "static/img/recordings/crops/" + str(dev.id) + "_" + str(cam.id) + "_"
                    f_name = f_name + str(area.id) + ".jpg"
                    area.occuppied = model.Detect(f_name)
        d_mtx.release()


def start(model_path = None, devices=None, gpu = False):
    global th_started
    global th
    
    if gpu:
        tweak_gpu()
    
    th = Thread(target = ai_thread_start, args = (model_path, devices))
    th.start()
    th_started = True
