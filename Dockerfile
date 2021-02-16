FROM tensorflow/tensorflow:latest-gpu


# Copy-paste commands:

# Building image
# docker build --tag theslipper/parkind .

# Deployment of Parkind
# cwdir="ai/dataset/"
# ddir=$(pwd)
# docker run -v "${ddir}/${cwdir}:/opt/Parkind/${cwdir}" -it --gpus=all --name parkind \
# --network host -p 127.0.0.1:8000:8000/tcp theslipper/parkind

# Training models
# cd ai/
# mkdir models/
# mkdir stats/
# python3 train.py -d --epochs 20

# Running the server
# 

# Removal of container and image
# docker rm parkind
# docker rmi theslipper/parkind


RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6' -y

RUN pip3 install --upgrade pip

RUN pip3 install Django==3.1.6
RUN pip3 install djangorestframework \
    markdown \
    django-filter \
    keras \
    opencv-python \
    matplotlib

# Create folder structure and 
# RUN mdkir -p /Parkind/ai/models/
WORKDIR /opt/Parkind

COPY ai/*.py /opt/Parkind/ai/
COPY manage.py /opt/Parkind/manage.py
COPY api/ /opt/Parkind/api/
COPY Parkind/ /opt/Parkind/Parkind/
COPY static/ /opt/Parkind/static/
COPY ui/ /opt/Parkind/ui/
COPY db.sqlite3 /opt/Parkind/db.sqlite3
# COPY . Parkind/

EXPOSE 8000/tcp
# RUN python3 /opt/Parkind/manage.py migrate
# RUN python3 manage.py createsuperuser
# RUN python3 Parkind/manage.py runserver
