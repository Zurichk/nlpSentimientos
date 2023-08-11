FROM python:3.10.0-alpine
#FROM python:3.10.0rc2-buster

RUN mkdir /usr/src/app/
COPY ./code /usr/src/app/
WORKDIR /usr/src/app/

#COPY ./requirements.txt /usr/src/app/requirements.txt
#RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

RUN apk update && apk add python3-dev gcc libc-dev linux-headers
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

#CMD ["flask", "run", "--host", "0.0.0.0"]