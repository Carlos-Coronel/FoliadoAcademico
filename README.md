# Proyecto Django

Este es un proyecto de Django que incluye instrucciones para el despliegue, instalación de dependencias, configuración de variables de entorno, y ejecución del servidor.

## Prerrequisitos

- Python 3.x
- pip (gestor de paquetes de Python)

## Instrucciones para el Despliegue

### 1. Clonar el Repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/usuario/proyecto-django.git
cd proyecto-django
```

### 2. Crear y Activar un Entorno Virtual

Es recomendable crear un entorno virtual para mantener las dependencias aisladas:

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

### 3. Instalar Dependencias

Instala las dependencias listadas en `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Renombra el archivo `.env_template` a `.env` y configura tus variables de entorno:

```bash
mv .env_template .env
```

Abre `.env` y añade tus valores específicos (como `DJANGO_SECRET_KEY` y otras configuraciones).


Para Genetrar el `SECRET_KEY` usar el siguiente comando en la consola 

```bash

python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

```
Esto generará una clave secreta segura, la cual debes copiar y pegar en el archivo  `.env.template ` 
o directamente en tu archivo  `.env ` bajo la variable  `SECRET_KEY`

### 5. Migraciones de la Base de Datos

Aplica las migraciones de la base de datos:

```bash
python manage.py migrate
```

### 6. Recopilar Archivos Estáticos

Para actualizar los archivos HTML o JS, ejecuta el comando `collectstatic`:

```bash
python manage.py collectstatic
```

### 7. Ejecutar el Servidor de Desarrollo

Inicia el servidor de desarrollo con el siguiente comando:

```bash
python manage.py runserver
```

Ahora deberías poder acceder a tu aplicación en `http://127.0.0.1:8000/`.

## Consideraciones Adicionales

- **Variables de Entorno Sensibles**: Asegúrate de que el archivo `.env` no se suba al control de versiones (agrega `.env` al archivo `.gitignore`).
- **Actualización de Dependencias**: Si necesitas actualizar las dependencias, puedes modificar `requirements.txt` y luego correr:

  ```bash
  pip install -r requirements.txt
  ```

## Contribuciones

Si deseas contribuir, por favor haz un fork del repositorio y envía un pull request. Agradecemos tus contribuciones para hacer de este proyecto algo mejor.

## Licencia

Este proyecto está bajo la Licencia MIT. 

---

¡Gracias por usar nuestro proyecto Django!
