# Parkind

Parkind is an easy to use intelligent open source parking managment server. The application provides a web interface for managing the connected devices running a [ParkindStreamer](https://github.com/TheSlipper/ParkindStreamer) instance and all of the relevant parking lot data. It is also capable of detecting free parking spots from the received video feed, allows the user to inspect the parking in real time and shares a rest API for other microsystems or microcontrollers.

**Warning:** Program is still in early stage of development. Some of the features are not yet implemented or are not stable. Please do not use this product in production

## Installation

This section will describe deploying the Parkind system in a docker container with the use of [tensorman](https://support.system76.com/articles/use-tensorman/).

1. Install docker and tensorman

```
sudo apt-get update && sudo apt-get install docker.io tensorman
```

2. Clone this repository

```
git clone https://github.com/TheSlipper/Parkind.git
```

3. Install the dependencies for the docker image

```
cd Parkind/
sudo tensorman run --gpu --python3 bash
pip install --upgrade pip
python -m pip install Django
pip install djangorestframework
pip install markdown       
pip install django-filter  
```

4. Set up the server

```
python manage.py migrate
python manage.py createsuperuser
```

5. Run the server and exit after finishing the execution

```
python manage.py runserver # press ctrl+c to exit it
exit
```

## Notice

The project is still in the workings - most of the features are not implemented yet.

## Description

The parkind project's goal is to create a set of open source tools that make it easier for parking owners to manage traffic load and parking fee acquisition. 

## Features

The project's main goals is to provide the features listed below:

* Parking lot occupancy detection for offloading traffic of some parts of parkings
* Detection and reading the license plates
* Providing a user friendly web interface for management of all the connected sensors and cameras
* Providing a JSON RESTful API for the applications to upload and download data
