FROM ubuntu:23.10

MAINTAINER buho_team "moren1viguel@gmail.com"

ENV LAST_UPDATED 2023-11-03

#ADD deploy.sh /

# Setup apt
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update

# Install required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq install -y -u python3 xorg xvfb dbus-x11 imagemagick xfonts-100dpi xfonts-75dpi xfonts-cyrillic curl ghostscript firefox xvfb dpkg openssh-server wget libpq-dev python3-dev python3-setuptools git-core python3-pip build-essential nano python3-psycopg2 libpangocairo-1.0-0

RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update


#upgrade de pip
RUN  pip3 install setuptools --upgrade
RUN pip3 install --upgrade pip
RUN pip3 install django-realtime --upgrade

RUN apt-get update -y
#RUN apt-get install -y tzdata

#UTF 8 Servidor
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ America/Bogota
#RUN ls
ADD requirements.txt /backend-waretrack/requirements.txt
RUN pip3 install -r /backend-waretrack/requirements.txt --ignore-installed


WORKDIR /backend-waretrack