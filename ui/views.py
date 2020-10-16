from django.shortcuts import render


# from api.models import *


# Login and Registration
def login(request):
    return render(request, 'ui/login.html')


def register(request):
    return render(request, 'ui/register.html')


def forgot_password(request):
    return render(request, 'ui/forgot_password.html')


# Dashboard
def dashboard(request):
    # Smi queries for GPU information:
    # https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries
    #
    # Query for utilization of GPU: nvidia-smi --query-gpu=utilization.gpu --format=csv

    return render(request, 'ui/dashboard.html')


# Devices views
def devices_list(request):
    # devices = Device.objects.order_by(sort_by)[page:elems]
    # ctx = {'devices': devices}
    return render(request, 'ui/devices/list.html')


def devices_requests(request):
    return render(request, 'ui/devices/device_requests.html')


def devices_api_inspection(request):
    return render(request, 'ui/devices/api_inspection.html')


def devices_add_form(request):
    # TODO: Switch to that when working with authentication and authorization
    # usr_id = {'user_id': request.user.id}
    usr_id = {'user_id': 1}
    return render(request, 'ui/devices/add_form.html', usr_id)


def devices_general_settings(request):
    return render(request, 'ui/devices/general_settings.html')


def devices_api_settings(request):
    return render(request, 'ui/devices/api_settings.html')


# Cameras views
def cameras_list(request):
    return render(request, 'ui/cameras/list.html')


def cameras_detection_areas(request):
    return render(request, 'ui/cameras/detection_areas.html')


def cameras_streaming_requests(request):
    return render(request, 'ui/cameras/requests.html')


def cameras_livestream(request):
    return render(request, 'ui/cameras/livestream.html')


def cameras_general_settings(request):
    return render(request, 'ui/cameras/general_settings.html')


def cameras_streaming_settings(request):
    return render(request, 'ui/cameras/streaming_settings.html')


def cameras_add_form(request):
    usr_id = {'user_id': 1}
    return render(request, 'ui/cameras/add_form.html', usr_id)


# Users
def users_list(request):
    return render(request, 'ui/users/user_list.html')


def users_role_list(request):
    return render(request, 'ui/users/role_list.html')


def users_ban_list(request):
    return render(request, 'ui/users/bans_list.html')


# Misc.
def misc_quick_start(request):
    return render(request, 'ui/misc/quick_start.html')


def misc_help(request):
    return render(request, 'ui/misc/help.html')
