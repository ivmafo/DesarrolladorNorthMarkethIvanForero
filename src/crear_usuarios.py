import sqlite3

def crear_usuarios_ejemplo():
    # Conectamos a la base de datos (la crea si no existe)
    conexion = sqlite3.connect('usuarios.db')
    cursor = conexion.cursor()
    
    # Creamos la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios_registrados (
            usuario TEXT PRIMARY KEY,
            clave TEXT NOT NULL
        )
    ''')
    
    # Lista de usuarios de ejemplo
    usuarios = [
        ('parcero', 'chevere123'),
        ('admin', 'admin123'),
        ('usuario1', 'pass123'),
        ('pepito', 'perez123'),
        ('juanita', 'flores456')
    ]
    
    # Insertamos los usuarios
    try:
        cursor.executemany('INSERT OR REPLACE INTO usuarios_registrados VALUES (?, ?)', usuarios)
        conexion.commit()
        print("¡Usuarios creados exitosamente!")
        
        # Mostramos los usuarios creados
        print("\nUsuarios disponibles:")
        print("-" * 30)
        cursor.execute('SELECT * FROM usuarios_registrados')
        for usuario in cursor.fetchall():
            print(f"Usuario: {usuario[0]}")
            print(f"Clave: {usuario[1]}")
            print("-" * 30)
            
    except sqlite3.Error as error:
        print(f"Error al crear usuarios: {error}")
    
    finally:
        conexion.close()

if __name__ == "__main__":
    crear_usuarios_ejemplo()