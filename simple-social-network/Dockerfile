FROM ubuntu:20.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    python3-pip

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
#RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


ENV TZ Asia/Tehran

# copy project


COPY . .