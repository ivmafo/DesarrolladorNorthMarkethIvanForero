import requests

class ServicioRickMorty:  
    def __init__(self):
        self.api_url = 'https://rickandmortyapi.com/api/character'
    
    def obtener_personajes(self):  
        response = requests.get(self.api_url)
        if response.status_code == 200:
            print(response.json()['results'])
            return response.json()['results'][:100]
        return []