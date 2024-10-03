import requests
import json
import os
from datetime import datetime, timedelta
import wikipediaapi

# URL de la API de API-FOOTBALL
API_URL = "https://v3.football.api-sports.io/teams"
HEADERS = {
    "x-rapidapi-host": "api-football.com",
    "x-rapidapi-key": "53b73863681b9afe10db4b943280a00e"
}

# Nombre del archivo JSON
JSON_FILE = "equipos_data.json"

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
            # Obtener datos de Wikipedia
            page = wiki_wiki.page(equipo['team']['name'])
            historia = page.text if page.exists() else "Historia no disponible"

            # Inicializa valores predeterminados
            apodo = "Apodo no disponible"
            presidente = "Presidente no disponible"
            vicepresidente = "Vicepresidente no disponible"
            cantidad_socios = "Cantidad no disponible"
            goleador_historico = "Goleador histórico no disponible"
            jugadores_historicos = []
            jugador_mas_partidos = "No disponible"
            jugador_mas_titulos = "No disponible"
            entrenador_mas_ganador = "No disponible"

            # Resumir historia si es demasiado larga
            if historia != "Historia no disponible" and len(historia) > 500:  # Por ejemplo
                historia = historia[:500] + '...'  # Resumir a los primeros 500 caracteres

            # Chequear secciones en la página de Wikipedia
            if page.exists():
                # Aquí puedes implementar lógica adicional para extraer datos específicos
                # como apodo, presidente, etc. a partir del texto de la página.

                # Por ejemplo, podrías buscar texto específico en la historia:
                if 'apodo' in historia.lower():
                    apodo = historia.split('apodo')[1].split('\n')[0].strip()  # Solo un ejemplo de búsqueda

                # Aquí puedes agregar más lógica para extraer los otros datos faltantes

            # Crear el diccionario del equipo
            equipo_info = {
                "nombre": equipo['team']['name'],
                "logo": equipo['team']['logo'],
                "historia": historia,
                "apodo": apodo,
                "director_tecnico": equipo.get('coach', {}).get('name', "Director técnico no disponible"),
                "presidente": presidente,
                "vicepresidente": vicepresidente,
                "cantidad_socios": cantidad_socios,
                "goleador_historico": goleador_historico,
                "jugadores_historicos": jugadores_historicos,
                "jugador_mas_partidos": jugador_mas_partidos,
                "jugador_mas_titulos": jugador_mas_titulos,
                "entrenador_mas_ganador": entrenador_mas_ganador,
                "estadio": {
                    "nombre": equipo.get('venue', {}).get('name', "Estadio no disponible"),
                    "direccion": equipo.get('venue', {}).get('address', "Dirección no disponible"),
                    "ciudad": equipo.get('venue', {}).get('city', "Ciudad no disponible"),
                    "capacidad": equipo.get('venue', {}).get('capacity', "Capacidad no disponible"),
                    "superficie": equipo.get('venue', {}).get('surface', "Superficie no disponible"),
                    "imagen": equipo.get('venue', {}).get('image', "Imagen no disponible")
                },
                "plantel_actual": equipo.get('players', [])
            }
            equipos_data.append(equipo_info)

        # Guardar datos en JSON
        with open(JSON_FILE, 'w') as json_file:
            json.dump(equipos_data, json_file, indent=4)

        print(f"Datos guardados en {JSON_FILE}")
    else:
        print("Error al obtener los datos de la API:", response.status_code)

if __name__ == "__main__":
    # Verifica si el archivo JSON ya existe y si es necesario actualizar
    if os.path.exists(JSON_FILE):
        last_modified = datetime.fromtimestamp(os.path.getmtime(JSON_FILE))
        if datetime.now() - last_modified > timedelta(days=2):
            fetch_data()
        else:
            print("No es necesario actualizar los datos.")
    else:
        fetch_data()
