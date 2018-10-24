FROM python:3.6
ENV PYTHONUNBUFFERED 1
MAINTAINER vixtel_of_hefei
RUN mkdir /www
WORKDIR /www
ADD ./requirements.txt /www/
RUN pip install -r requirements.txt
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo 'Asia/Shanghai' >/etc/timezone




