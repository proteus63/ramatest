from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from tmdbv3api import TMDb, Search

app = Flask(__name__)

# Configurazione di TMDB
tmdb = TMDb()
tmdb.api_key = '8b32222ed5da2fa7ff31e7ab08c8f64d'
search = Search()

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

# Route per gestire la richiesta del catalogo di serie coreane
@app.route('/catalog/series/rama-oriental-corea.json')
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
    
    return jsonify({
        "metas": metas
    })

# Avvio del server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
