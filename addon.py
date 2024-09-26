from flask import Flask, jsonify, request

app = Flask(__name__)

# Definiamo le informazioni sull'add-on
addon_manifest = {
    "id": "org.ramaorientalfansub.tv",
    "version": "0.0.1",
    "name": "Rama Oriental Fansub",
    "description": "Addon per Rama Oriental",
    "resources": ["catalog", "stream", "meta"],
    "types": ["movie", "series"],
    "catalogs": [{"type": "movie", "id": "rama_movies"}, {"type": "series", "id": "rama_series"}],
    "idPrefixes": ["rama"]
}

# Endpoint che restituisce il manifest dell'add-on
@app.route('/manifest.json')
def manifest():
    return jsonify(addon_manifest)

# Endpoint per restituire il catalogo (lista di film/serie)
@app.route('/catalog/<type>/<id>.json')
def catalog(type, id):
    if type == "movie" and id == "rama_movies":
        catalog_data = {
            "metas": [
                {"id": "movie1", "name": "Film 1", "poster": "url_poster", "type": "movie"},
                {"id": "movie2", "name": "Film 2", "poster": "url_poster", "type": "movie"},
            ]
        }
        return jsonify(catalog_data)
    elif type == "series" and id == "rama_series":
        catalog_data = {
            "metas": [
                {"id": "series1", "name": "Serie 1", "poster": "url_poster", "type": "series"},
                {"id": "series2", "name": "Serie 2", "poster": "url_poster", "type": "series"},
            ]
        }
        return jsonify(catalog_data)
    else:
        return jsonify({"metas": []})

# Endpoint per restituire i metadati di un film/serie specifico
@app.route('/meta/<type>/<id>.json')
def meta(type, id):
    meta_data = {
        "meta": {
            "id": id,
            "name": f"{type.capitalize()} {id}",
            "poster": "url_poster",
            "type": type,
            "description": f"Descrizione di {type.capitalize()} {id}"
        }
    }
    return jsonify(meta_data)

# Endpoint per restituire i flussi di streaming
@app.route('/stream/<type>/<id>.json')
def stream(type, id):
    streams = {
        "streams": [
            {"title": "Server 1", "url": "https://url_streaming1.com"},
            {"title": "Server 2", "url": "https://url_streaming2.com"}
        ]
    }
    return jsonify(streams)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
