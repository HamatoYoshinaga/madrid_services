from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Configuración del navegador
options = webdriver.ChromeOptions()
# options.add_argument(
#     "--headless"
# )  # Opcional: ejecutar en segundo plano (sin interfaz gráfica)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)  # Asegúrate de tener ChromeDriver instalado
driver.get("https://www.comunidad.madrid/etiquetas/consultorio")

# Cargar todos los consultorios haciendo clic en "Ver más"
while True:
    try:
        # Buscar el botón "Ver más" usando un selector confiable
        ver_mas_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//ul[contains(@class, 'pager-load-more')]//a[contains(text(), 'Ver más')]",
                )
            )
        )

        # Desplazar la página hacia el botón "Ver más"
        driver.execute_script("arguments[0].scrollIntoView(true);", ver_mas_button)
        time.sleep(2)  # Esperar un poco para asegurar que el botón esté visible

        # Asegurarse de que el botón es clicable con JavaScript
        driver.execute_script(
            "arguments[0].click();", ver_mas_button
        )  # Hacer clic usando JavaScript
        print("Clic en 'Ver más'.")
        time.sleep(3)  # Esperar que se cargue el contenido adicional

    except Exception as e:
        print("No hay más botones de 'Ver más' o se produjo un error:", e)
        break

# Extraer todos los enlaces de los consultorios
consultorios_links = set()  # Usamos un set para evitar duplicados
consultorios = driver.find_elements(
    By.XPATH, "//a[contains(@href, '/centros')]"
)  # Ajustar XPath si es necesario

for consultorio in consultorios:
    consultorios_links.add(consultorio.get_attribute("href"))

driver.quit()

# Mostrar los resultados
print(f"Se encontraron {len(consultorios_links)} enlaces únicos.")
for enlace in consultorios_links:
    print(enlace)

with open(
    "output_data/link_consultorios.csv", "w", newline="", encoding="utf-8"
) as file:
    writer = csv.writer(file)
    writer.writerow(["Enlace"])
    for enlace in consultorios_links:
        writer.writerow([enlace])

print("Enlaces exportados a output_data/link_consultorios.csv.")
