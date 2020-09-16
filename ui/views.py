from django.shortcuts import render


# Dashboard
def dashboard(request):
    return render(request, 'ui/dashboard.html')


# Devices views
def devices_list(request):
    return render(request, 'ui/devices/list.html')


def devices_requests(request):
    return render(request, 'ui/devices/device_requests.html')


def devices_api_inspection(request):
    return render(request, 'ui/devices/api_inspection.html')


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
