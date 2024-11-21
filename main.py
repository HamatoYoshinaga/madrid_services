import pandas as pd
import geopandas as gpd

# Leer csv, este csv viene con datos de todos los años desde 1996
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
# Esta linea sirve para extraer los nombres de los municipios del dataframe
# pero por ahora no nos hace falta
# df["Municipios"] = df["Municipios"].str.extract(r"([a-zA-ZñÑáéíóúÁÉÍÓÚ\s,]+)")

# Importar fichero shapefile con pyshp
# sf = shapefile.Reader("input_data/DatosNmc/nucl2023.shp")
# list(sf.fields)

# for feat in sf.iterShapeRecords():
#     print(feat.record["ETIQUETA"])

# Importar fichero shapefile de nucleos urbanos con geopandas
gdf = gpd.read_file("input_data/DatosNmc/nucl2023.shp")
# Filtrar por nucleos sin la etiqueta 'Diseminado'
gdf["CDNUCLEO"] = gdf["CDNUCLEO"].astype(int)
gdf = gdf[gdf["CDNUCLEO"] != 99]

# Juntar las dos tablas de censo y shapefile
df.rename(columns={"Total": "poblacion_mun"}, inplace=True)
df["poblacion_mun"] = df["poblacion_mun"].apply(
    lambda x: int(x.replace(".", ""))
)  # quitar puntos y pasar a int
df = df[["poblacion_mun", "CMUN"]]
gdf["CMUN"] = gdf["CMUN"].astype(int)
gdf = gdf.merge(df, on="CMUN")

# Descartar nucleos urbanos que pertenecen a municipios con más de 50k habitantes
gdf = gdf.drop(columns=["CDENTIDAD", "CDNUCLEO", "CDTNUCLEO", "DESCR", "BUSCA"])
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
    nuc_hospital_pairs.sort_values(["nuc_id", "distance"]).groupby("nuc_id").head(2)
)

# Drop duplicate geometry columns from 'gdf' and 'hospitals' before merging
# nearest_hospitals = nearest_hospitals.drop(
#     columns=["geometry_nuc", "geometry_hospital"]
# )

# # Merge back with original GeoDataFrames to include all town and hospital information
# nearest_hospitals = nearest_hospitals.merge(
#     gdf[["mun_id", "geometry"]], on="mun_id", suffixes=("", "_town")
# )
# nearest_hospitals = nearest_hospitals.merge(
#     hospitals[["hospital_id", "geometry"]],
#     on="hospital_id",
#     suffixes=("_mun", "_hospital"),
# )

# The result contains each town with its two nearest hospitals and all their information

print(nearest_hospitals)
