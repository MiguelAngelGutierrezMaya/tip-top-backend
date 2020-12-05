# TIP TOP

![](https://test.tiptopenglish.co/media/icon-tiptop.png)

**Tabla de contenido**

[TOC]

#Especificación técnica de variables
##Archivos de entorno
La configuración de las variables de entorno se explican a continuación:
- **DJANGO_APP_URL**: Ruta de la aplicación frontend
- **DJANGO_MEDIA_URL**: Ruta de los archivos media
- **DJANGO_SETTINGS_MODULE**: Modulo de configuración de Django valor por defecto: *"tip_top_backend.settings.local"*
- **DJANGO_SECRET_KEY**: Llave secreta de la aplicación
- **DJANGO_ADMIN_URL**: Ruta del administrador de Django
- **DJANGO_ALLOWED_HOSTS**: Host permitidos para la comunicación con el api
-**DJANGO_CORS_ORIGIN_WHITELIST**: Host en lista blanca para acceder a comunicaciones con el rest framework
- **NOTIFIER_EMAIL**: email para envío de notificaciones
- **NOTIFIER_NAME**: Nombre de cabeza de notificaciones, por defecto: *"Tip-Top-English"*
- **USERNAME_SMTP**: Usuario smtp
- **PASSWORD_SMTP**: Contraseña del usuario smtp
- **HOST_SMTP**: Servicio host del smtp
- **PORT_SMTP**: Puerto del servicio

#Proceso de instalación
Verificar la instalación de la base de datos postgresql y configurar las credenciales en los archivos de entorno (desarrollo o producción)

Ejecutar el siguiente comando (tener en cuenta el entorno en el que se encuentra, desarrollo o producción):

`$ docker-compose -f docker-compose.production.yml up -d --build`

Establecer las migraciones iniciales

`$ docker-compose -f docker-compose.production.yml run --rm django python manage.py migrate`

Agregar los primeros datos requeridos por defecto en la Base de datos para las tablas roles, documentos, ciudades, estados y paises

Crear el usuario superadmin

`$ docker-compose -f docker-compose.production.yml run --rm django python manage.py createsuperuser`

Si te encuentras en la instalación en un entorno de producción, debes configurar las tareas programadas en el servicio cron del vps, un ejemplo se muestra a continuación:

`$ crontab -e`

Pegar el texto que se encuentra en el archivo `.cronjobs` de la carpeta `.envs/.production/` al final

Reinicializar el servicio de tareas

`$ sudo service cron restart`
