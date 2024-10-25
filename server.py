import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from waitress import serve

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProgramaAcademico.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    print(f"Error al configurar WSGI: {e}")
    exit(1)

# Obtén la ruta completa al directorio de archivos estáticos
STATIC_DIR = os.path.join(settings.BASE_DIR, 'static')

# Verifica si el directorio existe
if os.path.isdir(STATIC_DIR):
    # Configura StaticFilesMiddleware para servir archivos estáticos
    from django.contrib.staticfiles.handlers import StaticFilesHandler
    application = StaticFilesHandler(application)

    # Inicia el servidor Waitress
    try:
        serve(application, host='172.26.1.115', port='8080', threads=8)
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
else:
    print(f"El directorio de archivos estáticos '{STATIC_DIR}' no existe.")
