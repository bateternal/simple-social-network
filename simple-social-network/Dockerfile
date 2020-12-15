FROM python:3

expose 8000
copy . /usr/src/app
WORKDIR /usr/src/app
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate



