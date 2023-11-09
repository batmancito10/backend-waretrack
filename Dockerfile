FROM python:3.11

LABEL maintainer="waretrack_team <moren1viguel@gmail.com>"

# Instalar paquetes y dependencias
RUN apt-get update && apt-get install -y \
    xorg xvfb dbus-x11 imagemagick xfonts-100dpi xfonts-75dpi curl ghostscript xvfb dpkg openssh-server wget libpq-dev libpangocairo-1.0-0 && \
    apt-get clean

# Configurar el entorno de tiempo
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV TZ=America/Bogota

# Copiar el archivo de requerimientos
COPY requirements.txt /backend-waretrack/requirements.txt

# Crear un directorio de trabajo
WORKDIR /backend-waretrack

# Instalar paquetes de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir