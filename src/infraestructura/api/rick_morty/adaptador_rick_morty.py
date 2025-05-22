import requests

class ServicioRickMorty:  
    def __init__(self):
        self.api_url = 'https://rickandmortyapi.com/api/character'
    
    def obtener_personajes(self):  # Changed from get_characters to match port interface
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()['results'][:100]
        return []