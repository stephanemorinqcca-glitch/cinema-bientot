import requests
import json
from datetime import datetime
import pytz

# Configuration
TOKEN = "shrfm72nvm2zmr7xpsteck6b64"
FILM_API_URL = "https://api.useast.veezi.com/v4/film"

# Fuseau horaire
tz = pytz.timezone('America/Toronto')
now = datetime.now(tz).date()

# Préparer la requête
headers = {
    "VeeziAccessToken": TOKEN,
    "Accept": "application/json",
    "Content-Type": "application/json"
}

try:
    response = requests.get(FILM_API_URL, headers=headers, timeout=10)
    response.raise_for_status()
    films = response.json()
except requests.exceptions.RequestException as e:
    print(f"❌ Erreur réseau : {e}")
    films = []

# Filtrer les films dont la date de sortie est plus tard qu'aujourd'hui
bientot_films = []
for film in films:
    release_date_str = film.get("OpeningDate")
    if release_date_str:
        try:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%dT%H:%M:%S").date()
            if release_date > now:
                bientot_films.append({
                    "id": film.get("Id"),
                    "titre": film.get("Title"),
                    "OpeningDate": release_date_str,
                    "synopsis": film.get("Synopsis", ""),
                    "classification": film.get("Rating", ""),
                    "duree": film.get("Duration", ""),
                    "genre": film.get("Genre", []),
                    "format": film.get("Format", ""),
                    "affiche": film.get("FilmPosterUrl", ""),
                    "thumbnail": film.get("FilmPosterThumbnailUrl", ""),
                    "banniere": film.get("BackdropImageUrl", ""),
                    "bande_annonce": film.get("FilmTrailerUrl", ""),
                    "content": film.get("Content", "")
                })
        except Exception as e:
            print(f"⚠️ Erreur de parsing de date pour {release_date_str} : {e}")

# Sauvegarder dans bientot.json
with open("bientot.json", "w", encoding="utf-8") as f:
    json.dump(bientot_films, f, ensure_ascii=False, indent=2)

print(f"✅ {len(bientot_films)} films enregistrés dans bientot.json.")
