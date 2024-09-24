from bs4 import BeautifulSoup
import requests

class RamaOrientalAddon:
    base_url = 'https://ramaorientalfansub.tv'

    @classmethod
    def get(cls, path):
        """Effettua una richiesta GET al sito"""
        url = f'{cls.base_url}{path}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
        except requests.ConnectionError:
            print("Errore di connessione")
        return None

    @classmethod
    def drama_detail(cls, path):
        """Ottieni i dettagli di un drama"""
        html_content = cls.get(path)
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Trova il poster
        poster = soup.find('div', class_='poster').find('img')['src']
        
        # Trova il titolo
        title = soup.find('h1', class_='entry-title').text.strip()
        
        # Trova la trama
        plot = soup.find('div', class_='entry-content').find('p').text.strip()
        
        # Trova i generi
        genre_elements = soup.find_all('a', href=True)
        genres = [a.text for a in genre_elements if '/genre/' in a['href']]

        return {
            'title': title,
            'poster': poster,
            'plot': plot,
            'genres': genres
        }

    @classmethod
    def search(cls, query):
        """Effettua una ricerca per titolo sul sito"""
        path = f"/?s={query}"  # Modifica l'URL di ricerca per ramaorientalfansub.tv
        html_content = cls.get(path)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        results = []

        # Trova i risultati di ricerca
        for item in soup.find_all('div', class_='result-item'):
            title = item.find('h2', class_='title').text.strip()
            poster = item.find('img')['src']
            link = item.find('a')['href']

            results.append({
                'title': title,
                'poster': poster,
                'link': link
            })
        return results

# Esempio di chiamata per ottenere i dettagli di un drama
rama_addon = RamaOrientalAddon()
drama_details = rama_addon.drama_detail('/drama/some-drama-path')
print(drama_details)

# Esempio di ricerca
search_results = rama_addon.search('azione')
print(search_results)
