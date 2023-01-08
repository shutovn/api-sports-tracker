FROM debian:latest
MAINTAINER Shutov Nikolay 'shutovnv@gmail.com'
RUN apt-get update -y && apt-get install -y python3 python3-pip python3-dev build-essential && apt-get autoremove && apt-get clean

COPY ./myapp /app

WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "entrypoint.sh"]
