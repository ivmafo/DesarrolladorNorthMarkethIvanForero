from abc import ABC, abstractmethod
from typing import List, Dict

class ServicioPersonajePort(ABC): 
    @abstractmethod
    def obtener_personajes(self) -> List[Dict]:
        pass