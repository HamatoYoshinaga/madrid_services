import csv
import requests
from bs4 import BeautifulSoup

# Configurar los archivos CSV
input_csv = "output_data/link_consultorios.csv"
output_csv = "output_data/consultorios_centros_salud.csv"

# Cargar datos del CSV de entrada
consultorios_data = []

with open(input_csv, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        consultorios_data.append(
            {"Consultorio": row["ETIQUETA"], "Enlace Consultorio": row["URL"]}
        )


# Función para extraer los datos del centro de salud
def extraer_datos_consultorio(enlace):
    try:
        response = requests.get(enlace)
        if response.status_code != 200:
            print(f"Error al cargar {enlace}: {response.status_code}")
            return {
                "Centro de Salud": "Error",
                "Enlace Centro de Salud": "No encontrado",
            }

        soup = BeautifulSoup(response.content, "html.parser")

        # Intentar encontrar un enlace directo al centro de salud
        centro_salud_element = soup.find(
            "a", href=lambda href: href and "/centros/centro-salud" in href
        )

        if centro_salud_element:
            centro_salud_nombre = centro_salud_element.text.strip()
            centro_salud_link = (
                "https://www.comunidad.madrid" + centro_salud_element["href"]
            )
        else:
            # Si no hay enlace directo, buscar dentro de un párrafo que contiene el nombre
            parrafos = soup.find_all(
                "p", string=lambda s: s and "centro de salud" in s.lower()
            )
            centro_salud_nombre = "No encontrado"
            centro_salud_link = "No encontrado"

            for parrafo in parrafos:
                # Si el párrafo no tiene enlace, extraemos el nombre del centro de salud directamente
                if "centro de salud" in parrafo.text.lower():
                    # Extracción del texto después de "Centro de Salud" o "centro de salud"
                    centro_salud_nombre_pueblo = (
                        parrafo.text.lower().split("centro de salud", 1)[-1].strip()
                    )
                    centro_salud_nombre = (
                        f"Centro de Salud {centro_salud_nombre_pueblo}"
                    )
                    centro_salud_link = "No disponible"  # No hay enlace disponible
                    break  # Una vez encontrado, salimos del bucle

        return {
            "Centro de Salud": centro_salud_nombre,
            "Enlace Centro de Salud": centro_salud_link,
        }
    except Exception as e:
        print(f"Error procesando {enlace}: {e}")
        return {"Centro de Salud": "Error", "Enlace Centro de Salud": "No encontrado"}


# Procesar cada consultorio
resultados = []

for consultorio in consultorios_data:
    nombre = consultorio["Consultorio"]
    enlace = consultorio["Enlace Consultorio"]

    print(f"Procesando: {nombre} ({enlace})")
    datos_centro_salud = extraer_datos_consultorio(enlace)

    resultado = {
        "Consultorio": nombre,
        "Enlace Consultorio": enlace,
        "Centro de Salud": datos_centro_salud["Centro de Salud"],
        "Enlace Centro de Salud": datos_centro_salud["Enlace Centro de Salud"],
    }

    resultados.append(resultado)

# Guardar resultados en un nuevo CSV
with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = [
        "Consultorio",
        "Enlace Consultorio",
        "Centro de Salud",
        "Enlace Centro de Salud",
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(resultados)

print(f"Datos guardados en {output_csv}")
