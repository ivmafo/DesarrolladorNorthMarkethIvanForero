import requests
from bs4 import BeautifulSoup

def buscar_productos(palabra_buscada):
    """
    Busca productos en MercadoLibre
    """
    palabra_buscada = palabra_buscada.replace(' ', '-').lower()
    url_base = f"https://listado.mercadolibre.com.co/{palabra_buscada}"
    
    print(f"\n[DEBUG] URL a consultar: {url_base}")  # Debug point 1
    
    cabeceras = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-CO,es;q=0.8',
    }
    
    try:
        respuesta = requests.get(url_base, headers=cabeceras, timeout=10)
        print(f"[DEBUG] Status Code: {respuesta.status_code}")
        
        sopa = BeautifulSoup(respuesta.content, 'lxml')
        
        # Actualizamos los selectores usando la estructura exacta del HTML
        productos_encontrados = sopa.select('ol.ui-search-layout--stack > li.ui-search-layout__item')
        
        if not productos_encontrados:
            print(f"\nBuscando: {palabra_buscada}")
            print("No encontré productos. ¿Probamos con otra palabra?")
            print(f"[DEBUG] Cantidad de productos encontrados: {len(productos_encontrados)}")
            return
        
        print(f"\nEncontré estos productos para: {palabra_buscada}\n")
        print("=" * 60)
        
        for i, producto in enumerate(productos_encontrados[:5], 1):
            # Selectores exactos según el HTML proporcionado
            nombre = producto.select_one('.poly-component__title')
            precio_actual = producto.select_one('.andes-money-amount__fraction')
            link = producto.select_one('.poly-component__title')
            envio = producto.select_one('.poly-component__shipping')
            
            if nombre and precio_actual:
                print(f"\nProducto #{i}")
                print(f"Nombre: {nombre.text.strip()}")
                print(f"Precio: ${precio_actual.text.strip()} COP")
                if link and link.parent.get('href'):
                    print(f"Link: {link.parent['href']}")
                if envio:
                    print(f"Envío: {envio.text.strip()}")
                print("-" * 60)
            
    except requests.Timeout:
        print("Lla página está demorando mucho en riesponder.")
    except requests.RequestException as error:
        print(f"Hubo un error de coneión!: {error}")
    except Exception as error:
        print(f"jubo un error inesperado!: {error}")

def main():
    print("¡Bienvenido al buscador de productos en MercadoLibre!")
    print("Puedes buscar cualquier producto y se mostrara los 5 primeros resultados.")
    
    while True:
        palabra_a_buscar = input("\n¿Qué quieres buscar? (o escribe 'salir' para terminar): ").strip()
        
        if not palabra_a_buscar:
            print("Escribe algo para buscar.")
            continue
            
        if palabra_a_buscar.lower() == 'salir':
            print("\nJhasta luego.")
            break
            
        buscar_productos(palabra_a_buscar)

if __name__ == "__main__":
    main()