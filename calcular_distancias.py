import pandas as pd
import geopandas as gpd

# Leer csv, este fichero viene con datos de todos los años desde 1996
# y con datos sobre la población masculina y femenina. Por eso lo filtramos
df = pd.read_csv(
    "input_data/censoCM_INE.csv",
    delimiter=";",
    engine="python",
)

# Filtrar por población Total y periodo 2023
df = df[df["Sexo"] == "Total"]
df = df[df["Periodo"] == 2023]
df = df[["Municipios", "Total"]]
# Corregir formato
df["CMUN28"] = df["Municipios"].str.extract(r"(\d+)").astype(int)
df["CMUN"] = df["CMUN28"] % 1000
# La siguiente linea sirve para extraer los nombres de los municipios del dataframe
# pero por ahora no nos hace falta
# df["Municipios"] = df["Municipios"].str.extract(r"([a-zA-ZñÑáéíóúÁÉÍÓÚ\s,]+)")

# Importar fichero shapefile de nucleos urbanos con geopandas
gdf = gpd.read_file("input_data/DatosNmc/nucl2023.shp")
# Filtrar por nucleos sin la etiqueta 'Diseminado'
gdf["CDNUCLEO"] = gdf["CDNUCLEO"].astype(int)
gdf = gdf[gdf["CDNUCLEO"] != 99]

# Formatear las tablas de censo y nucleos urbanos
df.rename(columns={"Total": "poblacion_mun"}, inplace=True)
df["poblacion_mun"] = df["poblacion_mun"].apply(
    lambda x: int(x.replace(".", ""))
)  # quitar puntos y pasar a int
df = df[["poblacion_mun", "CMUN"]]
gdf["CMUN"] = gdf["CMUN"].astype(int)
# Unir las dos tablas
gdf = gdf.merge(df, on="CMUN")

# Descartar nucleos urbanos que pertenecen a municipios con más de 50k habitantes
gdf = gdf.drop(columns=["CDENTIDAD", "CDNUCLEO", "DESCR", "BUSCA"])
gdf = gdf[gdf["poblacion_mun"] <= 50000]

# Ordenar la tabla por municipios
gdf.sort_values(by="CMUN", ascending=True, inplace=True)
gdf = gdf.set_index("ETIQUETA")

# Calcular centroides de nucleos urbanos
gdf["polygon"] = gdf["geometry"]
gdf["geometry"] = gdf.geometry.centroid

# importar fichero con hospitales
hospitals = gpd.read_file("input_data/DatosNmc/hospital.shp")
# hospitals = hospitals.drop(
#     columns=[
#         "URL",
#         "CD_VIA",
#         "MUNICIPIO",
#         "DIRECCION",
#         "CMUN",
#         "BUSCA",
#         "DESCR",
#         "CODIGO",
#         "UTM_X",
#         "UTM_Y",
#     ]
# )

hospitals = hospitals.set_index("ETIQUETA")
# Antes de calcular las distancias nos aseguramos que los GeoDataFrames tienen el mismo CRS
gdf = gdf.to_crs(hospitals.crs)

# Añadir los identificadores que queremos conservar
gdf["nuc_id"] = gdf.index
hospitals["hospital_id"] = hospitals.index

# Realizar una unión cartesiana de modo que obtengamos
# todas las combinaciones de nucleo urbano y hospital
nuc_hospital_pairs = gdf[["nuc_id", "geometry"]].merge(
    hospitals[["hospital_id", "geometry"]], how="cross", suffixes=("_nuc", "_hospital")
)

# Calculamos la distancia para cada par de hospital y nucleo urbano
# axis=1 sirve para que la función aplique sobre la misma fila
# con axis=0 (valor predeterminado) aplicaría a una misma columna
nuc_hospital_pairs["distance"] = nuc_hospital_pairs.apply(
    lambda row: row["geometry_nuc"].distance(row["geometry_hospital"]), axis=1
)

# Ordenamos la tabla por núcleos y distancias, de esta forma se mostrarán los núcleos
# urbanos con sus hospitales más cercanos primero. Agrupamos por núcleos y nos quedamos
# solo con los dos primeros

nearest_hospitals = (
    nuc_hospital_pairs.sort_values(["nuc_id", "distance"]).groupby("nuc_id").head(6)
)

# Volver a unir con las tablas originales para preservar alguna información necesaria
nearest_hospitals = nearest_hospitals.merge(
    gdf[["CDTNUCLEO", "CMUN", "nuc_id"]], on="nuc_id", suffixes=("", "_nuc")
)

nearest_hospitals = nearest_hospitals.merge(
    hospitals[["CODIGO", "hospital_id"]],
    on="hospital_id",
    suffixes=("", "_hospital"),
)

print("writing csv...")
# Convertir la geometría a WKT
gdf_csv = nearest_hospitals.copy()
gdf_csv["geometry_nuc"] = gdf_csv["geometry_nuc"].apply(lambda x: x.wkt if x else None)
gdf_csv["geometry_hospital"] = gdf_csv["geometry_hospital"].apply(
    lambda x: x.wkt if x else None
)

# Guardar como CSV para visualizar el output
output_path = "output_data/distancias_nuc_hos.csv"
gdf_csv.to_csv(output_path, index=False)
print(f"output saved to {output_path}")
