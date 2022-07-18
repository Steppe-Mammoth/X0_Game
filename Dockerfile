FROM python:3.10

WORKDIR /home/ubuntu/docker/XO

COPY requirements.txt /home/ubuntu/docker/XO

RUN pip install -r /home/ubuntu/docker/XO/requirements.txt

COPY . /home/ubuntu/docker/XO