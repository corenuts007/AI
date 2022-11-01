# syntax=docker/dockerfile:1

FROM python:3.10.7

#ENV PYTHONUNBUFFERED True

#ENV APP_HOME /app
#WORKDIR $APP_HOME
WORKDIR /ai-python
ADD . /

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY . ./

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


#CMD [ "python", "-m", "run"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app