from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configurar Selenium
options = Options()
options.add_argument("--headless")  # Quitar si querés ver el navegador
service = Service()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# Lista para almacenar datos
productos = []

for pagina in range(1, 23):  # 1 a 22 inclusive
    url = f"https://www.herrafe.com/productos/{pagina}/relevancia/productos/marcas/nx-1361s1-cerrajeria/etiquetas/variantes/precios/codigos-dinamicos"
    print(f"Scrapeando página {pagina}...")
    driver.get(url)

    try:
        # Esperar a que los productos carguen
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'product-item-with-carousel')))
        time.sleep(2)  # por si tarda en renderizar
    except Exception as e:
        print(f"No se pudieron cargar los productos en la página {pagina}: {e}")
        continue

    # Obtener los elementos de productos
    productos_html = driver.find_elements(By.TAG_NAME, 'product-item-with-carousel')

    for producto in productos_html:
        try:
            html_raw = producto.get_attribute('outerHTML')
            print("\n============================")
            print("HTML del producto:")
            print(html_raw)
            print("============================\n")

            # Nombre
            nombre = producto.find_element(By.CSS_SELECTOR, 'div.text-sm span').text.strip()

            # Imagen desde <source srcset="..."> dentro de <picture>
            try:
                srcset = producto.find_element(By.CSS_SELECTOR, 'optimized-image-container source').get_attribute('srcset')
                imagen = 'https://www.herrafe.com' + srcset if srcset else None
            except:
                imagen = None


            productos.append({
                'nombre': nombre,
                'url_imagen': imagen
            })

        except Exception as e:
            print(f"Error extrayendo producto: {e}")
            continue

driver.quit()

# Guardar como DataFrame
df = pd.DataFrame(productos)
print(df.head)
df.to_excel(r"C:\Users\primo\Desktop\Ciencia de Datos\Proyectos\Open\productos_urlimagen.xlsx", index=False)