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
    films = None  # Indique qu'on ne doit pas continuer

# Filtrer les films dont la date de sortie est plus tard qu'aujourd'hui
bientot_films = []
for film in films:
    # ❌ API ne fournit pas de Title, arrêt du process
    titre = film.get("Title")
    if not titre:
        print("❌ API ne fournit pas de Title, arrêt du process.")
        sys.exit(1)  # Arrêt complet du script
    
    release_date_str = film.get("OpeningDate")
    if release_date_str:
        try:
            release_date = datetime.strptime(release_date_str, "%Y-%m-%dT%H:%M:%S").date()
            national_code = film.get("NationalCode", "")
            
            # Exclure les films avec NationalCode == "0"
            if release_date > now and national_code != "0":
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
                    "content": film.get("Content", ""),
                })
        except Exception as e:
            print(f"⚠️ Erreur de parsing de date pour {release_date_str} : {e}")

# 🔽 Tri par date croissante
bientot_films.sort(key=lambda x: datetime.strptime(x["OpeningDate"], "%Y-%m-%dT%H:%M:%S"))

    # Écriture du fichier seulement si films est valide
    with open("bientot.json", "w", encoding="utf-8") as f:
        json.dump(bientot_films, f, ensure_ascii=False, indent=4)
        print(f"✅ {len(bientot_films)} films enregistrés dans bientot.json.")
else:
    print("⏩ Aucun changement apporté à bientot.json (ou erreur réseau).")
