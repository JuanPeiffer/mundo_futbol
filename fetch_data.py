import os
import django
import requests
import json
from datetime import datetime, timedelta
import wikipediaapi
from django.conf import settings
from urllib import request

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mundo_futbol.settings')
django.setup()

# Ahora puedes importar tus modelos
from equipos.models import EquipoFutbol

# URL de la API de API-FOOTBALL
API_URL = "https://v3.football.api-sports.io/teams"
HEADERS = {
    "x-rapidapi-host": "api-football-v1.p.rapidapi.com",
    "x-rapidapi-key": "53b73863681b9afe10db4b943280a00e"
}

# Nombre del archivo JSON
JSON_FILE = "equipos_data.json"
ESCUDOS_FOLDER = os.path.join(settings.MEDIA_ROOT, 'escudos', '128')  # Carpeta de escudos

# Inicializa Wikipedia API con user_agent y lenguaje
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MundoFutbolApp/1.0 (juampybj2013@gmail.com)',  # Cambia esto con tu email
    language='es'
)

def fetch_data():
    # Parámetros necesarios para la solicitud
    params = {
        "league": "128",  # Cambia según la liga que desees consultar
        "season": "2024"  # Cambia según la temporada que desees consultar
    }
    
    response = requests.get(API_URL, headers=HEADERS, params=params)
    print("Código de estado:", response.status_code)
    print("Contenido de la respuesta:", response.text)  # Muestra la respuesta

    if response.status_code == 200:
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Error al decodificar la respuesta JSON.")
            return

        equipos_data = []
        for equipo in data['response']:
            # Ajustar la búsqueda de la historia del equipo
            team_name = equipo['team']['name']
            # Intentar obtener la historia usando el nombre del equipo
            page = wiki_wiki.page(team_name)
            
            # Si no existe la página, buscar un nombre alternativo
            if not page.exists():
                # Ejemplo de un nombre alternativo (puedes agregar más según sea necesario)
                alternate_name = team_name.replace(" ", "_")  # Reemplaza espacios con guiones bajos
                page = wiki_wiki.page(f"Club Atlético {alternate_name}")

            historia = page.text if page.exists() else "Historia no disponible"
            
            # Obtener el apodo
            apodo = equipo['team'].get('nickname', "Apodo no disponible")

            # Guardar escudo en la carpeta local
            logo_url = equipo['team']['logo']
            logo_filename = f"{equipo['team']['id']}.png"  # Nombre del archivo con el ID del equipo
            logo_path = os.path.join(ESCUDOS_FOLDER, logo_filename)

            # Crea la carpeta si no existe
            os.makedirs(ESCUDOS_FOLDER, exist_ok=True)

            # Descargar el logo
            request.urlretrieve(logo_url, logo_path)

            # Crear o actualizar el equipo en la base de datos
            equipo_obj, created = EquipoFutbol.objects.update_or_create(
                nombre=team_name,
                defaults={
                    "logo": logo_path,  # Guardar el path local del logo
                    "ciudad": equipo.get('venue', {}).get('city', "Ciudad no disponible"),
                    "historia": historia,
                    "apodo": apodo,
                    "director_tecnico": equipo.get('coach', {}).get('name', "Director técnico no disponible"),
                    "presidente": "Presidente no disponible",  # Reemplaza si tienes estos datos
                    "vicepresidente": "Vicepresidente no disponible",  # Reemplaza si tienes estos datos
                    "cantidad_socios": None,  # Reemplaza si tienes estos datos
                    "goleador_historico": "Goleador histórico no disponible",  # Reemplaza si tienes estos datos
                    "jugadores_historicos": [],  # Reemplaza si tienes estos datos
                    "jugador_mas_partidos": "No disponible",  # Reemplaza si tienes estos datos
                    "jugador_mas_titulos": "No disponible",  # Reemplaza si tienes estos datos
                    "entrenador_mas_ganador": "No disponible",  # Reemplaza si tienes estos datos
                    "estadio": equipo.get('venue', {}).get('name', "Estadio no disponible"),
                    "plantel_actual": equipo.get('players', [])
                }
            )
            
            # Agregar todos los datos del equipo al JSON
            equipos_data.append({
                "nombre": equipo_obj.nombre,
                "logo": logo_path,
                "ciudad": equipo_obj.ciudad,
                "historia": equipo_obj.historia,
                "apodo": equipo_obj.apodo,
                "director_tecnico": equipo_obj.director_tecnico,
                "presidente": equipo_obj.presidente,
                "vicepresidente": equipo_obj.vicepresidente,
                "cantidad_socios": equipo_obj.cantidad_socios,
                "goleador_historico": equipo_obj.goleador_historico,
                "jugadores_historicos": equipo_obj.jugadores_historicos,
                "jugador_mas_partidos": equipo_obj.jugador_mas_partidos,
                "jugador_mas_titulos": equipo_obj.jugador_mas_titulos,
                "entrenador_mas_ganador": equipo_obj.entrenador_mas_ganador,
                "estadio": equipo_obj.estadio,
                "plantel_actual": equipo_obj.plantel_actual
            })

        # Guardar datos en JSON
        with open(JSON_FILE, 'w') as json_file:
            json.dump(equipos_data, json_file, indent=4)

        print(f"Datos guardados en {JSON_FILE} y base de datos actualizada.")
    else:
        print("Error al obtener los datos de la API:", response.status_code)


if __name__ == "__main__":
    fetch_data()
