from abc import ABC, abstractmethod
from dominio.modelo.usuario import Usuario

class RepositorioUsuarioPort(ABC):  
    @abstractmethod
    def obtener_por_nombre_usuario(self, username: str) -> Usuario:  # Changed from get_by_username
        pass
    
    @abstractmethod
    def guardar(self, usuario: Usuario):  # Changed from save
        pass
    
    @abstractmethod
    def validar_credenciales(self, username: str, password: str) -> bool:  # Already in Spanish
        pass