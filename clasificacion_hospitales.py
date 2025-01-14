import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
import difflib


def normalizar_nombre(nombre):
    nombre = (
        unicodedata.normalize("NFKD", nombre).encode("ascii", "ignore").decode("utf-8")
    )
    nombre = " ".join(nombre.split())
    return nombre.lower()


def obtener_grupo_hospitales(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    hospitales = {}

    grupos = {
        "hospitales-gran-complejidad": "Grupo 3",
        "hospitales-complejidad-intermedia": "Grupo 2",
        "hospitales-baja-complejidad": "Grupo 1",
    }

    for div_id, grupo in grupos.items():
        div_grupo = soup.find("div", id=div_id)
        for hospital in div_grupo.find_all("h3"):
            nombre_hospital = hospital.find("a").text.strip()
            hospitales[normalizar_nombre(nombre_hospital)] = grupo

    return hospitales


def encontrar_nombre_mas_similar(nombre, lista_nombres):
    mejor_coincidencia = difflib.get_close_matches(
        nombre, lista_nombres, n=1, cutoff=0.9
    )
    return mejor_coincidencia[0] if mejor_coincidencia else None


def actualizar_csv_con_grupo(hospitales_csv, hospitales_dict):
    df = pd.read_csv(hospitales_csv)

    # Normalizar nombres en el DataFrame
    df["nombre_hospital_normalizado"] = df["ETIQUETA"].apply(normalizar_nombre)

    # Crear una lista de nombres de hospitales disponibles para comparar
    lista_hospitales = list(hospitales_dict.keys())

    # Buscar la mejor coincidencia para cada hospital
    df["nombre_hospital_corregido"] = df["nombre_hospital_normalizado"].apply(
        lambda x: encontrar_nombre_mas_similar(x, lista_hospitales)
    )

    # Añadir la columna 'grupo' basándose en el nombre corregido
    df["grupo"] = (
        df["nombre_hospital_corregido"].map(hospitales_dict).fillna("No clasificado")
    )

    # Guardar el nuevo archivo CSV
    df.drop(
        columns=["nombre_hospital_normalizado", "nombre_hospital_corregido"]
    ).to_csv("output_data/hospitales_actualizado.csv", index=False)

    # Generar un reporte de hospitales clasificados
    clasificados = df[df["grupo"] != "No clasificado"]
    clasificados.to_csv("output_data/hospitales_clasificados.csv", index=False)


if __name__ == "__main__":
    url = "https://www.comunidad.madrid/servicios/salud/hospitales-red-servicio-madrileno-salud"
    hospitales_dict = obtener_grupo_hospitales(url)
    actualizar_csv_con_grupo("output_data/hospitales.csv", hospitales_dict)
