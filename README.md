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






#### ###### ###
 





# usb_ferias

### Abrir Web Local

    docker-compose -f local.yml up -d

### Cerrar Web Local

    docker-compose -f local.yml down

### Crear Nuevo Branch

    Desde la terminal crear nuevo branch a partir del ultimo branch

### Crear Build Local (Guardar codigo)

    docker-compose -f local.yml up -d --build

### Agregar cambios a Git

    git add .
    git commit -m "Mensaje"
    git push

### Actualizar mi codigo local desde Git

    git pull

### Crear usuario desde Docker

    docker-compose -f local.yml run --rm django python manage.py createsuperuser
