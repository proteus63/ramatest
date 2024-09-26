import requests
from bs4 import BeautifulSoup
from tmdbv3api import TMDb, Search
from stremio_addon_sdk import Addon, manifest
import logging

logging.basicConfig(level=logging.INFO)

# Configurazione di TMDB
tmdb = TMDb()
tmdb.api_key = 'LA_TUA_API_KEY_TMDB'

search = Search()

# Creazione dell'addon con manifest per Stremio
addon = Addon(manifest={
    "id": "community.ramaorientalfansub",
    "version": "1.0.0",
    "name": "Rama Oriental Fansub Addon",
    "description": "Addon per mostrare contenuti di Corea del Sud da Rama Oriental Fansub con TMDB integration",
    "types": ["series", "movie"],
    "catalogs": [
        {"type": "series", "id": "rama-oriental-corea", "name": "Serie Coreane"},
    ],
    "resources": [
        "catalog"
    ]
})

# Funzione di scraping per raccogliere i titoli delle serie da Rama Oriental Fansub
def scrape_ramaorientalfansub():
    url = "https://ramaorientalfansub.tv/paese/corea-del-sud/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    shows = []
    for item in soup.find_all('div', class_='post-list-item'):
        title = item.find('h2', class_='entry-title').get_text(strip=True)
        link = item.find('a')['href']
        shows.append({
            'title': title,
            'link': link
        })
    
    return shows

# Funzione per ottenere metadati da TMDB utilizzando i titoli delle serie
def get_tmdb_metadata(title):
    result = search.tv(query=title)
    
    if result:
        show = result[0]
        return {
            "id": f"tmdb-{show.id}",
            "name": show.name,
            "type": "series",
            "poster": f"https://image.tmdb.org/t/p/w500{show.poster_path}" if show.poster_path else None,
            "description": show.overview,
            "background": f"https://image.tmdb.org/t/p/original{show.backdrop_path}" if show.backdrop_path else None,
            "year": show.first_air_date.split("-")[0] if show.first_air_date else "N/A",
        }
    return None

# Handler per il catalogo delle serie coreane
@addon.route('/catalog/series/rama-oriental-corea.json')
def catalog_handler():
    scraped_shows = scrape_ramaorientalfansub()
    
    metas = []
    for show in scraped_shows:
        # Cerca i metadati TMDB per ogni show
        metadata = get_tmdb_metadata(show['title'])
        if metadata:
            metas.append(metadata)
        else:
            # Se non trova metadati su TMDB, aggiungi solo il titolo e il link
            metas.append({
                "id": show['link'],
                "name": show['title'],
                "type": "series",
                "poster": None,
                "description": "Non disponibile su TMDB",
                "background": None,
                "year": "N/A"
            })
    
    return {
        "metas": metas
    }

# Avvio del server dell'addon
if __name__ == "__main__":
    addon.serve('http://0.0.0.0:5555')
