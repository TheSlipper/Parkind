from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Device
from .serializers import DeviceSerializer


@api_view(['GET'])
def device_list(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def device_detail(request, id):
    devices = Device.objects.get(id=id)
    serializer = DeviceSerializer(devices, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def device_create(request):
    serializer = DeviceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201)

    return HttpResponse(status=400)


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
