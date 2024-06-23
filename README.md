# Juan Futbol

Mundo Futbol es un proyecto sobre el fútbol desarrollado con Django.

## Instalación

Sigue estos pasos para configurar y ejecutar el proyecto localmente.

### Requisitos Locales:

- Python 3.x
- pip (el gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

### Configuración del Entorno Virtual

1. Crea Apps

    python manage.py startapp [NOMBRE]

2. Prende Local

    python manage.py runserver

3. Atualiza base de datos

    python manage.py makemigrations  
    python manage.py migrate  

4. Usa Plantilla html:

    {% extends 'base.html' %}
    {% block content %}
    contenido
    {% endblock %}