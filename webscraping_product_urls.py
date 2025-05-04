from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

# Configuración del WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

url = "https://www.herrafe.com/productos/22/relevancia/productos/marcas/nx-1361s1-cerrajeria/etiquetas/variantes/precios/codigos-dinamicos"
driver.get(url)
time.sleep(5)

productos_info = []

# Detectar cantidad total de productos
total_productos = len(driver.find_elements(By.TAG_NAME, 'product-item-with-carousel'))
print(f"🔍 Total detectado: {total_productos} productos.")

for i in range(total_productos):
    try:
        print(f"\n➡ Procesando producto {i + 1}...")

        productos_actuales = driver.find_elements(By.TAG_NAME, 'product-item-with-carousel')
        producto = productos_actuales[i]

        # Casos especiales: productos sin imagen que no se puede scrapear con esta técnica
        if i == 88:
            print("⚠ Producto con comportamiento especial (sin imagen).")
            nombre = producto.text.strip()
            print(f"✅ {nombre}\n🔗 URL no encontrado")
            productos_info.append({
                "Producto": nombre,
                "URL Producto": "URL no encontrado"
            })
            continue

        # Scroll hacia el producto
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", producto)
        time.sleep(1)

        # Clic
        print("⏳ Haciendo clic...")
        ActionChains(driver).move_to_element(producto).click().perform()
        time.sleep(3)

        # Obtener datos
        url_producto = driver.current_url
        nombre = driver.find_element(By.TAG_NAME, "h1").text.strip()
        print(f"✅ {nombre}\n🔗 {url_producto}")

        productos_info.append({
            "Producto": nombre,
            "URL Producto": url_producto
        })

        # Volver atrás y esperar
        driver.back()
        time.sleep(3)

    except Exception as e:
        print(f"❌ Error procesando producto {i + 1}: {e}")

# Cerrar navegador y exportar
driver.quit()
df = pd.DataFrame(productos_info)
df.to_excel("debug_click_productos_pagina22.xlsx", index=False)
print("\n✅ Archivo generado: 'debug_click_productos_pagina22.xlsx'")
