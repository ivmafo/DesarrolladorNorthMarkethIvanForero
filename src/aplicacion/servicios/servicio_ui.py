from dominio.modelo.usuario import Usuario

class ServicioUI:  
    def __init__(self, usuario_repository, personaje_service):
        self.usuario_repository = usuario_repository
        self.personaje_service = personaje_service
        
    def validar_login(self, username, password):
        if not username or not password:
            raise ValueError("Nombre de usuario y contraseña requeridos")
        return self.usuario_repository.validar_credenciales(username, password)
    
    def usuario_existe(self, username):
        return self.usuario_repository.obtener_por_nombre_usuario(username) is not None
    
    def registrar_usuario(self, username, password):
        if not username or not password:
            raise ValueError("Nombre de usuario y contraseña requeridos")
        
        if self.usuario_existe(username):
            raise ValueError("El usuario ya existe")
            
        self.usuario_repository.guardar(Usuario(username, password))
    
    def obtener_personajes(self):
        return self.personaje_service.obtener_personajes()