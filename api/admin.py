from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Notification)
admin.site.register(DashboardSettings)
admin.site.register(Device)
admin.site.register(DeviceRequestHistory)
admin.site.register(Camera)
admin.site.register(ParkingArea)