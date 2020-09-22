from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    """
    Notification for a user.
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
    Settings of the user's dashboard design.
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

