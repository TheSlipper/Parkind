FROM tensorflow/tensorflow:latest-gpu

# docker build --tag theslipper/parkind .
# docker run -it --gpus=all --name parkind --network host -p 127.0.0.1:8000:8000/tcp theslipper/parkind
# docker rm parkind

RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

RUN pip3 install --upgrade pip

RUN pip3 install Django \
    djangorestframework \
    markdown \
    django-filter \
    keras \
    opencv-python

COPY . Parkind/

RUN python3 Parkind/manage.py migrate
EXPOSE 8000/tcp
# RUN python3 manage.py createsuperuser
# RUN python3 Parkind/manage.py runserver
