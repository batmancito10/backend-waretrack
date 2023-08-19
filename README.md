# Backend-waretrack :alien:
## Proyecto Backend - waretrack

**Instalación**


> Asegurarte de tener Python instalado en tu computadora

> Crear un entorno virtual de Python para el proyecto

	python -m venv venv

> Activamos el entorno virtual:

	.\venv\Scripts\activate

> Instalamos todas las dependencias requeridas para Waretrack:

	pip install -r requirements.txt

Creamos nuestro archivo `.env` para crear las variables de entrono recuerda tiene que ser en en la carpeta donde esta el archivo `settings.py`

> En el archivo `.env` agregamos las variables

	DEBUG=valor
	SECRET_KEY=valor
	DB_NAME=valor
	DB_USER=valor
	DB_PASSWORD=valor
	DB_HOST=valor
	DB_PORT=valor

## ya puedes correr el proyecto :ok_hand:

	python manage.py runserver

Copyright &copy; Waretrack