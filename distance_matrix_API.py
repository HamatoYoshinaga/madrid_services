import pandas as pd
import geopandas as gpd
import googlemaps
import ast  # Para convertir listas en strings a listas reales

# Configurar la API de Google (coloca tu API Key aquí)
API_KEY = "TU_API_KEY"
gmaps = googlemaps.Client(key=API_KEY)


def cargar_coordenadas_municipios(archivo):
    """
    Carga las coordenadas del centroide de los municipios en un diccionario
    """
    gdf = gpd.read_file(archivo)

    # Calcular el centroide
    gdf["centroide"] = gdf.geometry.centroid
    gdf = gdf.to_crs(epsg=4326)
    # Extraer latitud y longitud
    gdf["centroide_lat"] = gdf["centroide"].y
    gdf["centroide_lon"] = gdf["centroide"].x
    # Asegurarse de que las columnas existan
    if (
        "CMUN" not in gdf.columns
        or "centroide_lat" not in gdf.columns
        or "centroide_lon" not in gdf.columns
    ):
        raise ValueError("Faltan columnas requeridas en el shapefile de municipios.")

    # Convertir 'CMUN' a string y agregar prefijo '28'
    gdf["lau_id"] = "28" + gdf["CMUN"].astype(str).str.zfill(3)

    return {
        row["lau_id"]: (row["centroide_lat"], row["centroide_lon"])
        for _, row in gdf.iterrows()
    }


def cargar_coordenadas_hospitales(archivo):
    """
    Carga las coordenadas de los hospitales en un diccionario
    """
    gdf = gpd.read_file(archivo)
    gdf = gdf.to_crs(epsg=4326)

    # Extraer latitud y longitud
    gdf["latitud"] = gdf["geometry"].y
    gdf["longitud"] = gdf["geometry"].x
    # Asegurarse de que las columnas existan
    if (
        "CODIGO" not in gdf.columns
        or "latitud" not in gdf.columns
        or "longitud" not in gdf.columns
    ):
        raise ValueError("Faltan columnas requeridas en el shapefile de municipios.")

    return {
        row["CODIGO"]: (row["latitud"], row["longitud"]) for _, row in gdf.iterrows()
    }


def cargar_coordenadas_concs(archivo):
    """
    Carga las coordenadas del centroide de los municipios en un diccionario
    """
    # Cargar los datos
    gdf = gpd.read_file(archivo)
    df = pd.read_csv("datos_recibidos/cons_cs_nombres.csv")

    # Normalizar los nombres a minúsculas
    df.rename(columns={"Nombre": "ETIQUETA"}, inplace=True)
    df["ETIQUETA"] = df["ETIQUETA"].str.lower().str.strip()
    gdf["ETIQUETA"] = gdf["ETIQUETA"].str.lower().str.strip()

    # Hacer el merge después de corregir nombres
    gdf = gdf.merge(df, on="ETIQUETA", how="left")

    gdf = gdf.to_crs(epsg=4326)

    # Extraer latitud y longitud
    gdf["latitud"] = gdf["geometry"].y
    gdf["longitud"] = gdf["geometry"].x
    # Asegurarse de que las columnas existan
    if (
        "ETIQUETA" not in gdf.columns
        or "latitud" not in gdf.columns
        or "longitud" not in gdf.columns
    ):
        raise ValueError("Faltan columnas requeridas en el shapefile de municipios.")

    return {
        row["Codigo"]: (row["latitud"], row["longitud"]) for _, row in gdf.iterrows()
    }


def obtener_distancia(origen, destinos):
    """Consulta la Distance Matrix API y devuelve la distancia en metros."""
    result = gmaps.distance_matrix(
        origins=[origen], destinations=[destinos], mode="driving"
    )
    try:
        return result["rows"][0]["elements"][0]["distance"][
            "value"
        ]  # Distancia en metros
    except (KeyError, IndexError, TypeError):
        return None  # Si la API no devuelve datos


# Cargar coordenadas desde archivos CSV
coordenadas_mun = cargar_coordenadas_municipios("input_data/DatosNmc/muni2023.shp")
coordenadas_hos = cargar_coordenadas_hospitales("input_data/DatosNmc/hospital.shp")
coordenadas_cs = cargar_coordenadas_concs("input_data/DatosNmc/centrosalud.shp")
coordenadas_con = cargar_coordenadas_concs("input_data/DatosNmc/consultoriosalud.shp")

# Leer el archivo de relaciones municipios - hospitales, centros y consultorios
df_relaciones = pd.read_csv("datos_recibidos/relacion_municipios_salud.csv")

# Convertir listas en strings a listas reales
df_relaciones["hospitales"] = df_relaciones["hospitales"].apply(ast.literal_eval)
df_relaciones["centros_salud"] = df_relaciones["centros_salud"].apply(ast.literal_eval)
df_relaciones["consultorios"] = df_relaciones["consultorios"].apply(ast.literal_eval)

# Lista para almacenar resultados
resultados = []

# Definir el precio por cada par origen-destino según Google
precio_por_elemento = (
    0.005  # USD (verifica el precio actual en la documentación de Google)
)

# Inicializar contador de elementos facturables
total_elementos = 0

for _, row in df_relaciones.iterrows():
    municipio_id = str(row["lau_id"])

    if municipio_id not in coordenadas_mun:
        print(f"el municipio {municipio_id} no tiene coordenadas asignadas")
        continue  # Saltar municipios sin coordenadas

    origen = coordenadas_mun[municipio_id]  # Coordenadas del municipio
    destino = []
    for categoria, diccionario in [
        ("hospitales", coordenadas_hos),
        ("centros_salud", coordenadas_cs),
        ("consultorios", coordenadas_con),
    ]:
        for lugar_id in row[categoria]:
            if lugar_id in diccionario:
                destino.append(
                    diccionario[lugar_id]
                )  # Coordenadas del hospital/centro/consultorio
                # distancia = obtener_distancia(origen, destino)
                # resultados.append([municipio_id, categoria, lugar_id, distancia])
                total_elementos += 1  # Contar el par municipio-destino
    break
# Estimar costo total incluyendo distancia en transporte público
costo_estimado = total_elementos * precio_por_elemento * 2

print(f"Total de elementos facturables: {total_elementos}")
print(f"Costo estimado: ${costo_estimado:.2f} USD")

# # Guardar resultados en un CSV
# df_resultado = pd.DataFrame(
#     resultados, columns=["municipio_id", "tipo", "destino_id", "distancia_metros"]
# )
# df_resultado.to_csv("distancias_municipios.csv", index=False)

# print(
#     "Cálculo de distancias completado. Datos guardados en 'distancias_municipios.csv'."
# )
