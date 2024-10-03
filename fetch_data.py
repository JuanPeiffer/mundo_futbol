import os
import django
import requests
import json
from datetime import datetime
import wikipediaapi
from django.conf import settings
from urllib import request
from bs4 import BeautifulSoup

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mundo_futbol.settings')
django.setup()

# Ahora puedes importar tus modelos
from equipos.models import EquipoFutbol, Jugador

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
    """Función para obtener datos de equipos de la API de API-FOOTBALL y TyC Sports."""
    params = {
        "league": "128",  # Cambia según la liga que desees consultar
        "season": "2024"  # Cambia según la temporada que desees consultar
    }

    response = requests.get(API_URL, headers=HEADERS, params=params)
    print("Código de estado:", response.status_code)

    if response.status_code == 200:
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Error al decodificar la respuesta JSON.")
            return

        equipos_data = []
        for equipo in data['response']:
            team_name = equipo['team']['name']
            page = wiki_wiki.page(team_name)

            if not page.exists():
                alternate_name = team_name.replace(" ", "_")
                page = wiki_wiki.page(f"Club Atlético {alternate_name}")

            historia = page.text if page.exists() else "Historia no disponible"
            apodo = equipo['team'].get('nickname', "Apodo no disponible")

            logo_url = equipo['team']['logo']
            logo_filename = f"{equipo['team']['id']}.png"
            logo_path = os.path.join(ESCUDOS_FOLDER, logo_filename)

            os.makedirs(ESCUDOS_FOLDER, exist_ok=True)
            request.urlretrieve(logo_url, logo_path)

            tyc_data = get_tycsports_data(team_name)

            # Procesar cantidad de socios
            cantidad_socios_valor = tyc_data.get('cantidad_socios')
            if cantidad_socios_valor is None or cantidad_socios_valor == "Cantidad de socios no disponible":
                cantidad_socios_valor = None
            else:
                try:
                    cantidad_socios_valor = int(cantidad_socios_valor.replace('.', ''))  # Remover puntos si existen
                except ValueError:
                    cantidad_socios_valor = None

            # Crear o actualizar el equipo en la base de datos
            equipo_obj, created = EquipoFutbol.objects.update_or_create(
                nombre=team_name,
                defaults={
                    "logo": logo_path,
                    "ciudad": equipo.get('venue', {}).get('city', "Ciudad no disponible"),
                    "historia": historia,
                    "apodo": tyc_data.get('apodo', apodo),
                    "director_tecnico": tyc_data.get('director_tecnico', equipo.get('coach', {}).get('name', "Director técnico no disponible")),
                    "presidente": tyc_data.get('presidente', "Presidente no disponible"),
                    "vicepresidente": tyc_data.get('vicepresidente', "Vicepresidente no disponible"),
                    "cantidad_socios": cantidad_socios_valor,
                    "goleador_historico": tyc_data.get('goleador_historico', "Goleador histórico no disponible"),
                    "jugadores_historicos": tyc_data.get('jugadores_historicos', []),
                    "jugador_mas_partidos": tyc_data.get('jugador_mas_partidos', "No disponible"),
                    "jugador_mas_titulos": tyc_data.get('jugador_mas_titulos', "No disponible"),
                    "entrenador_mas_ganador": tyc_data.get('entrenador_mas_ganador', "No disponible"),
                    "estadio": equipo.get('venue', {}).get('name', "Estadio no disponible"),
                }
            )

            # Agregar jugadores al plantel actual
            for position, players in tyc_data.get('plantel', {}).items():
                for player_name in players:
                    Jugador.objects.update_or_create(
                        nombre=player_name,
                        equipo=equipo_obj,
                        posicion=position
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
                "plantel_actual": list(equipo_obj.jugadores.values_list('nombre', flat=True))
            })

        # Guardar datos en JSON
        try:
            with open(JSON_FILE, 'w') as json_file:
                json.dump(equipos_data, json_file, indent=4)
            print(f"Datos guardados en {JSON_FILE} y base de datos actualizada.")
        except Exception as e:
            print(f"Error al guardar los datos en JSON: {e}")

    else:
        print("Error al obtener los datos de la API:", response.status_code)

def safe_find_next(soup, search_text):
    """Función para buscar un texto y obtener el siguiente elemento, manejando errores."""
    try:
        element = soup.find(text=search_text)
        return element.find_next().text.strip() if element else None
    except Exception as e:
        print(f"Error buscando {search_text}: {e}")
        return None

def get_tycsports_data(team_name):
    """Función para obtener datos de TyC Sports."""
    base_url = "https://www.tycsports.com"
    formatted_name = team_name.lower().replace(' ', '-').replace('.', '').replace('\'', '').replace('&', 'y')
    team_url = f"{base_url}/{formatted_name}.html"

    print(f"Accediendo a: {team_url}")

    try:
        response = requests.get(team_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraer información del equipo
            apodo = safe_find_next(soup, 'Apodo')
            director_tecnico = safe_find_next(soup, 'Director Técnico') or safe_find_next(soup, 'Entrenador')
            presidente = safe_find_next(soup, 'Presidente')
            vicepresidente = safe_find_next(soup, 'Vicepresidente')
            cantidad_socios_valor = safe_find_next(soup, 'Cantidad de socios')

            # Asegúrate de que la variable no sea None antes de convertir
            if cantidad_socios_valor is not None:
                cantidad_socios_valor = cantidad_socios_valor.replace('.', '')  # Remover puntos si existen
            else:
                cantidad_socios_valor = "Cantidad de socios no disponible"  # Valor por defecto

            jugadores_historicos = safe_find_next(soup, 'Jugadores históricos')
            goleador_historico = safe_find_next(soup, 'Goleador histórico')
            jugador_mas_partidos = safe_find_next(soup, 'Jugador con más partidos')
            jugador_mas_titulos = safe_find_next(soup, 'Jugador con más títulos')
            entrenador_mas_ganador = safe_find_next(soup, 'Entrenador más ganador de la historia')
            estadio = safe_find_next(soup, 'Estadio')

            # Plantel
            plantel_arqueros = [arq.text.strip() for arq in soup.find(text='Arqueros').find_next('ul').find_all('li')] if soup.find(text='Arqueros') else []
            plantel_defensores = [defensor.text.strip() for defensor in soup.find(text='Defensores').find_next('ul').find_all('li')] if soup.find(text='Defensores') else []
            plantel_mediocampistas = [mediocampista.text.strip() for mediocampista in soup.find(text='Mediocampistas').find_next('ul').find_all('li')] if soup.find(text='Mediocampistas') else []
            plantel_delanteros = [delantero.text.strip() for delantero in soup.find(text='Delanteros').find_next('ul').find_all('li')] if soup.find(text='Delanteros') else []

            return {
                "apodo": apodo,
                "director_tecnico": director_tecnico,
                "presidente": presidente,
                "vicepresidente": vicepresidente,
                "cantidad_socios": cantidad_socios_valor,
                "goleador_historico": goleador_historico,
                "jugadores_historicos": jugadores_historicos.split(',') if jugadores_historicos else [],
                "jugador_mas_partidos": jugador_mas_partidos,
                "jugador_mas_titulos": jugador_mas_titulos,
                "entrenador_mas_ganador": entrenador_mas_ganador,
                "estadio": estadio,
                "plantel": {
                    "Arqueros": plantel_arqueros,
                    "Defensores": plantel_defensores,
                    "Mediocampistas": plantel_mediocampistas,
                    "Delanteros": plantel_delanteros
                }
            }
        else:
            print(f"Error al acceder a {team_url}: {response.status_code}")
            return {}
    except requests.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return {}

if __name__ == "__main__":
    fetch_data()
