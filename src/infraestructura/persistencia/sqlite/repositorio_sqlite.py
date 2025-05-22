import sqlite3
from dominio.modelo.usuario import Usuario
from dominio.puertos.salida.repositorio_usuario_port import RepositorioUsuarioPort

class RepositorioSQLite(RepositorioUsuarioPort):
    def __init__(self, db_name='usuarios.db'):
        self.db_name = db_name
        self._create_table()
    
    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios_registrados (
                    usuario TEXT PRIMARY KEY,
                    clave TEXT NOT NULL
                )
            ''')
            conn.commit()
    
    def obtener_por_nombre_usuario(self, username):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios_registrados WHERE usuario = ?', (username,))
            result = cursor.fetchone()
            return Usuario(result[0], result[1]) if result else None
    
    def guardar(self, usuario):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios_registrados VALUES (?, ?)', 
                         (usuario.username, usuario.password))
            conn.commit()
    
    def validar_credenciales(self, username, password):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios_registrados WHERE usuario = ? AND clave = ?', 
                         (username, password))
            return cursor.fetchone() is not None