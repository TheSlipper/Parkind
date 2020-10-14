from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """
    Model containing data on a user's notification.
    """
    id = models.AutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_on = models.DateField(null=False)
    icon_bg_type = models.CharField(default='success', null=False, max_length=30)
    icon_type = models.CharField(default='file', null=False, max_length=30)
    message = models.CharField(default='Notification message content', max_length=100)
    redirect_url = models.CharField(default='#', null=False, max_length=100)


class DashboardSettings(models.Model):
    """
    Model containing settings of a user's dashboard design.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Top data tiles
    gpu_load = models.BooleanField(default=True, null=False)
    top_statistic_tiles = models.BooleanField(default=True, null=False)

    # Occupation data
    occupation_overview = models.BooleanField(default=True, null=False)
    occupation_as_table = models.BooleanField(default=False, null=False)

    # GPU Usage
    gpu_usage_overview = models.BooleanField(default=True, null=False)
    gpu_usage_as_table = models.BooleanField(default=False, null=False)

    # Misc
    help_pane = models.BooleanField(default=True, null=False)
    contribution_pane = models.BooleanField(default=True, null=False)


class Device(models.Model):
    """
    Model containing information on a single IoT device connected to the Parkind system via its API.
    """
    id = models.AutoField(primary_key=True, null=False)
    ip_address = models.CharField(max_length=16, unique=True, null=False, default='255.255.255.255')
    created_on = models.DateField(null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(default='Parkind Device', null=False, max_length=100)
    description = models.TextField(default='An IoT device connected to the Parkind system via its API', null=False)
    request_logging = models.BooleanField(default=True, null=False)
    # api_permissions = models.ManyToManyField(ApiPermissions) - instead of this just add the settings to this table
    # as you find out what permissions will be available


class DeviceRequestHistory(models.Model):
    """
    Model containing information on a single API request made by a device with the request_logging flag set to true.
    """
    id = models.AutoField(primary_key=True, null=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    received_on = models.DateField(null=False)
    request_code = models.CharField(null=False, max_length=30)
    request_content = models.TextField()


class Camera(models.Model):
    """
    Model containing information on a camera connected to an IoT device which is connected to Parkind.
    """
    id = models.AutoField(primary_key=True, null=False)
    created_on = models.DateField(null=False)
    name = models.CharField(default='Parkind Camera', null=False, max_length=100)
    description = models.TextField(default='A camera connected to an IoT device that is connected to the Parkind '
                                           'system via its API', null=False)
    parent_device = models.ForeignKey(Device, on_delete=models.CASCADE)
    video_height = models.IntegerField(null=False)
    video_width = models.IntegerField(null=False)
    video_fps = models.IntegerField()


class ParkingArea(models.Model):
    """
    Information on the position and size of a parking area in the image of a given camera.
    """
    id = models.AutoField(primary_key=True, null=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)
    width = models.IntegerField(null=False)
    height = models.IntegerField(null=False)

