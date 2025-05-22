from infraestructura.persistencia.sqlite.repositorio_sqlite import RepositorioSQLite
from infraestructura.api.rick_morty.adaptador_rick_morty import ServicioRickMorty
from aplicacion.servicios.servicio_ui import ServicioUI
from infraestructura.ui.tkinter.vistas.ventana_principal import VentanaPrincipal

def main():
    # Inicializar adaptadores
    repositorio_sqlite = RepositorioSQLite()
    servicio_personajes = ServicioRickMorty()
    
    # Inicializar servicios
    servicio_ui = ServicioUI(repositorio_sqlite, servicio_personajes)
    
    # Inicializar UI
    app = VentanaPrincipal(servicio_ui)
    app.iniciar()

if __name__ == "__main__":
    main()