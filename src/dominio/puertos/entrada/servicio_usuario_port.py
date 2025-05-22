from abc import ABC, abstractmethod

class ServicioUsuarioPort(ABC): 
    @abstractmethod
    def registrar_usuario(self, username: str, password: str):
        pass

    @abstractmethod
    def validar_login(self, username: str, password: str) -> bool:
        pass