import requests
from bs4 import BeautifulSoup

# URL base
base_url = "https://www.comunidad.madrid/etiquetas/consultorio?page="

# Iterar por las páginas y extraer enlaces
consultorios_links = []
page = 0
max_pages = 16  # Limitar el número de páginas por seguridad

while page < max_pages:  # Evitar bucles infinitos
    print(f"Procesando página {page}...")
    response = requests.get(base_url + str(page))

    # Verificar que la solicitud sea exitosa
    if response.status_code != 200:
        print(f"Error al cargar la página {page}: {response.status_code}")
        break

    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar los enlaces en la página actual
    nuevos_links = [
        link["href"]
        for link in soup.find_all("a", href=True)
        if "/centros" in link["href"]
    ]

    # Si no hay nuevos enlaces, hemos llegado al final
    if not nuevos_links:
        print("No se encontraron más enlaces. Fin del scraping.")
        break

    # Agregar nuevos enlaces (convertir a absolutos si es necesario)
    consultorios_links.extend(
        [
            "https://www.comunidad.madrid" + link if link.startswith("/") else link
            for link in nuevos_links
        ]
    )

    # Incrementar la página
    page += 1

print(f"Se encontraron {len(consultorios_links)} enlaces.")
print(consultorios_links)
