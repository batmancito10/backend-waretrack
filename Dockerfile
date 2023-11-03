FROM ubuntu:23.10

MAINTAINER buho_team "moren1viguel@gmail.com"

ENV LAST_UPDATED 2023-11-03

# Setup apt
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update

# Install required packages
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq install -y -u python3 xorg xvfb dbus-x11 imagemagick xfonts-100dpi xfonts-75dpi xfonts-cyrillic curl ghostscript firefox xvfb dpkg openssh-server wget libpq-dev python3-dev python3-setuptools git-core python3-pip build-essential nano python3-psycopg2 libpangocairo-1.0-0

# Instalar python3-setuptools usando apt
RUN apt-get install -y python3-setuptools

# Actualizar pip
RUN pip3 install --upgrade pip

# Instalar paquetes de Python
RUN pip3 install django-realtime --upgrade

# Configurar entorno de tiempo
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=America/Bogota

# Copiar el archivo de requerimientos e instalar paquetes de Python
ADD requirements.txt /backend-waretrack/requirements.txt
RUN pip3 install -r /backend-waretrack/requirements.txt --ignore-installed

# Limpiar la caché de paquetes
RUN apt-get clean

WORKDIR /backend-waretrack