"""
WSGI config for ProgramaAcademico project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Establecer la ruta al entorno virtual (modifica la versión de Python según sea necesario)
venv_path = '/home/app/foliado/venv/lib/python3.10/site-packages'

# Agregar el directorio de site-packages del entorno virtual al PYTHONPATH
sys.path.append(venv_path)

# Agregar el directorio de tu proyecto al PYTHONPATH
sys.path.append('/home/app/foliado')

# Establecer la variable de entorno DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProgramaAcademico.settings')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Captura y registra el error (puedes usar el logging de Django o imprimir a un log)
    print(f"Error al cargar la aplicación WSGI: {e}", file=sys.stderr)
    raise

