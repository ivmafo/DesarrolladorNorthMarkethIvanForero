from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import tempfile # Import tempfile
import shutil # Import shutil

# Inicializa el navegador
# Create Chrome options
chrome_options = Options()
# Crea directorio temporal para user data
user_data_dir = tempfile.mkdtemp()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

# para optios al driver
driver = webdriver.Chrome(options=chrome_options)


# Inicia sesión en Instagram
driver.get('https://www.instagram.com/accounts/login/')
time.sleep(10)
driver.find_element(By.NAME, 'username').send_keys('ivmafo@hotmail.com') # ponga aqui su correo
driver.find_element(By.NAME, 'password').send_keys('Iforero2011.') # ponga aqui su contraseña
driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
time.sleep(10)

# Lista de cuentas a analizar
cuentas = ['elcorteingles', 'mercadona', 'carrefoures']

# Lista para almacenar los datos
datos = []

# Recorre cada cuenta
for cuenta in cuentas:
    # La url que muestra los seguidores /cuenta/followers/
    driver.get(f'https://www.instagram.com/{cuenta}/followers/')
    time.sleep(10)

    # La ruta XPath para Instagram.
    # '//a[contains(@href, "/followers/")]' que es el patron ppara el modal de seguidores
    # A menudo, necesitas hacer clic en el elemento que muestra el número de seguidores para abrir la ventana modal.
    # try:
    #     followers_element = driver.find_element(By.XPATH, f'//a[@href="/{cuenta}/followers/"]')
    #     followers_element.click()
    #     time.sleep(3) # Dale tiempo para que la ventana modal cargue
    # except Exception as e:
    #     print(f"No se pudo encontrar o hacer clic en el enlace de seguidores para {cuenta}: {e}")
    #     continue # Saltar a la siguiente cuenta si no podemos acceder a los seguidores

    # Una vez que la ventana modal de seguidores esté abierta (asumiendo que el clic funcionó), entonces debería iterar a través de los seguidores visibles.
    # La extracción de detalles de seguidores generalmente requiere desplazar la ventana modal de seguidores y extraer información de cada elemento de la lista.
    seguidores_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/followers/")]') 

    # se intenta encontrar el elemento que activa la ventana modal de seguidores y hacer clic en él.

    try:
        # busca el link que tenga algun followers
        followers_link_on_profile = driver.find_element(By.XPATH, f'//a[@href="/{cuenta}/followers/"]')
        followers_link_on_profile.click()
        time.sleep(10) # Expera a que cargue el modal  aunque solo el usuario dueño de la cuenta podra ver todos sus seguidores
        # la api de meta ya no permite ver todos los seguidores desde 2024 , habria que  tener business de instagram

        # en este punto se bre algun modal con una lista de seguidores
        follower_items = driver.find_elements(By.XPATH, '//div[@role="dialog"]//li') # Example: Find list items within the dialog

        print(f"Encotro {len(follower_items)} seguidores de la cuenta {cuenta}")

        # Iterar a través de estos elementos encontrados (que representan seguidores en la ventana modal)
        # Esto sigue siendo una suposición sobre la estructura y qué datos están disponibles de inmediato sin hacer clic en cada perfil.
        # La ventana modal de Instagram muestra el nombre de usuario y quizás un pequeño fragmento de biografía, pero no la biografía completa, 
        # el teléfono o el correo electrónico directamente.
        # Extraer el teléfono/correo electrónico de fragmentos de biografía en una ventana modal no es fiable y es difícil.
        # Intentar obtener la biografía completa, el teléfono, el correo electrónico y la fecha de creación implica navegar a cada perfil, lo cual algo dificil

        # Aqui se busca obtener datos de los elementos de la lista *dentro* de la ventana modal.
        for item in follower_items:
            try:
                # Este es un intento por buscar elementos dentro de cada elemento de la lista. que referencia un seguidor
                # Ejemplo: intentar encontrar el enlace del nombre de usuario dentro del elemento. a href
                nombre_element = item.find_element(By.XPATH, './/a') 
                nombre = nombre_element.text # obtener el texto del enlace

                # Intentar encontrar directamente la biografía/teléfono/correo electrónico dentro del elemento de la ventana modal es poco probable que funcione de manera fiable.
                # Estos campos suelen encontrarse en la página de perfil completa.
                # Los estableceremos como 'None' o un marcador de posición, ya que no podemos obtenerlos fácilmente de la ventana modal.
                bio = "N/A (from modal)"
                telefono = None
                email = None

                # Encontrar la fecha de creación desde la ventana modal tampoco es posible.
                fecha_creacion = "N/A" # Not available from modal list

                # Añade los datos a la lista
                datos.append([nombre, telefono, email, fecha_creacion])

                # Opcional: Desplazar la ventana modal para cargar más seguidores si es necesario (se requiere una lógica de desplazamiento más compleja)
                # driver.execute_script("arguments[0].scrollIntoView(false);", item)
                time.sleep(10) # Pausa breve después de desplazarse

            except Exception as item_error:
                print(f"No se pudo extraer datos de {cuenta}: {item_error}")
                continue # Continue al siguiente item si no se pueden extraer datos de este

    except Exception as account_error:
        print(f"No se pudo abrir la ventana modal de seguidores para la {cuenta}: {account_error}")
        continue # salta a la siguiente cuenta si no podemos abrir la ventana modal de seguidores


# Cierra el navegador
driver.quit()

# Elimina el directorio temporal de datos de usuario
#shutil.rmtree(user_data_dir)


# Crea un DataFrame de pandas
df = pd.DataFrame(datos, columns=['Nombre', 'Teléfono', 'Email', 'Fecha de Creación'])

# Guarda los datos en un archivo Excel
df.to_excel('seguidores_instagram.xlsx', index=False)