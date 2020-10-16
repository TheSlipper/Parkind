from rest_framework import serializers
from .models import *


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceRequestHistory
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'
