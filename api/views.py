from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


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
