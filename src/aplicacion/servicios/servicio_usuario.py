from dominio.modelo.usuario import Usuario

class ServicioUsuario:
    def __init__(self, usuario_repository):
        self.repository = usuario_repository
    
    def registrar_usuario(self, username, password):
        if not username or not password:
            raise ValueError("Nombre de usuario y contraseña requeridos")
        
        usuario_existe = self.repository.obtener_por_nombre_usuario(username)
        if usuario_existe:
            raise ValueError("El usuario ya existe")
        
        new_user = Usuario(username, password)
        self.repository.guardar(new_user)
    
    def validar_login(self, username, password):
        return self.repository.validar_credenciales(username, password)