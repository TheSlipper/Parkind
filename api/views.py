from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from threading import Thread

from .models import *
from .serializers import *
# from ai import * as ai
import ai
import _thread


import numpy as np
import cv2

th = None

# Device CRUD
@api_view(['POST'])
def device_create(request, token):
    # TODO: Token is that the device generates and user inputs. Verify if the device uses that token in here
    serializer = DeviceSerializer(data=request.data)
    user = request.user

    # TODO: Uncomment this once logging in system works
    if serializer.is_valid():  # and user.id == serializer.validated_data.created_by:
        serializer.save()
        return HttpResponse(status=201)

    return HttpResponse(status=400)


@api_view(['GET'])
def device_detail(request, id):
    devices = Device.objects.get(id=id)
    serializer = DeviceSerializer(devices, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def device_list(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def device_update(request, id):
    device = Device.objects.get(id=id)
    serializer = DeviceSerializer(instance=device, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=200)

    return HttpResponse(status=400)


@api_view(['DELETE'])
def device_delete(request, id):
    device = Device.objects.get(id=id)
    device.delete()
    return HttpResponse(status=200)


@csrf_exempt
def device_check(request):
    # get the data
    post_data = request.body.decode('utf-8').split('&')
    url = post_data[0]
    token = post_data[1]
    
    # Send to the device
    resp = requests.post(url, data = 'token=' + token)

    print(resp.text)

    pass

# Device request RD
@api_view(['GET'])
def device_request_detail(request, id):
    device_request = DeviceRequestHistory.objects.get(id=id)
    serializer = DeviceRequestSerializer(device_request, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def device_request_list(request):
    device_requests = DeviceRequestHistory.objects.all()
    serializer = DeviceRequestSerializer(device_requests, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def device_request_delete(request, id):
    device_request = DeviceRequestHistory.objects.get(id=id)
    device_request.delete()
    return HttpResponse(status=200)


# Detection area CRUD
@api_view(['POST'])
def detection_area_create(request):
    serializer = DetectionAreaSerializer(data=request.data)

    if serializer.is_valid():
        obj = serializer.save()
        return HttpResponse(str(obj.id), content_type='text/plain', status=201)

    return HttpResponse(status=400)


@api_view(['GET'])
def detection_area_detail(request, id):
    detection_area = ParkingArea.objects.get(id=id)
    serializer = DetectionAreaSerializer(detection_area, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def detection_area_list(request):
    detection_areas = ParkingArea.objects.all()
    serializer = DetectionAreaSerializer(detection_areas, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def detection_area_delete(request, id):
    detection_area = ParkingArea.objects.get(id=id)
    detection_area.delete()
    return HttpResponse(status=200)


# Camera CRUD
@api_view(['POST'])
def camera_create(request):
    serializer = CameraSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201)

    return HttpResponse(status=400)


@api_view(['GET'])
def camera_detail(request, id):
    cameras = Camera.objects.get(id=id)
    serializer = CameraSerializer(cameras, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def camera_list(request):
    cameras = Camera.objects.all()
    serializer = CameraSerializer(cameras, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def camera_update(request, id):
    camera = Camera.objects.get(id=id)
    serializer = CameraSerializer(instance=camera, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=200)

    return HttpResponse(status=400)


@api_view(['DELETE'])
def camera_delete(request, id):
    camera = Camera.objects.get(id=id)
    camera.delete()
    return HttpResponse(status=200)


# Frame/AI endpoints
@csrf_exempt
def init_ai(request):
    if ai.started():
        return HttpResponse(status=202)

    
    # Set up objects
    model_path = ""
    dev_objs = Device.objects.all()
    cam_objs = Camera.objects.all()
    parea_objs = ParkingArea.objects.all()
    devices = []

    for dev in dev_objs:
        cameras = []
        for cam in cam_objs:
            if cam.parent_device == dev.id:
                areas = []
                for area in parea_objs:
                    if area.camera == cam.id:
                        areas.append(ai.DetectionArea(area.id, None, False))
                camera = ai.Camera(cam.id, areas)
                cameras.append(camera)
        device = ai.Device(dev.id, cameras)
        devices.append(device)

    # Set up the thread and run it
    # TODO: Perhaps extract gpu from GET
    # TODO: Load model from some settings or GET
    ai.start("models/InceptionV3/", devices, True)

    return HttpResponse(status=202)


@csrf_exempt
def frame_upload(request, dev_id, cam_id):
    # Decode and save image to disk
    img = cv2.imdecode(np.fromstring(request.body, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    f_name = str(dev_id) + "_" + str(cam_id) + "_" + datetime.now().strftime("%d/%m/%Y %H:%M:%S.jpg")
    cv2.imwrite("ai_data/img/" + f_name, img)

    # Get rectangle data
    darea_objs = ParkingArea.objects.filter(camera=cam_id)
    rects = []
    for area in darea_objs:
        rect = ai.Rect(area.x, area.y, area.width, area.height)
        rects.append(rect)

    # Update the frame for the AI module
    res = ai.update_frame(img, dev_id, cam_id, detection_areas)
    if res:
        return HttpResponse(status=202)
    else:
        return HttpResponse(status=400)
