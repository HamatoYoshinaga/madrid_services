import pandas as pd

distancias = pd.read_csv("output_data/distancia_min_nuc_hos.csv")
censo = pd.read_csv("input_data/censoCM_edades.csv", index_col="CMUN", delimiter=";")

# Borramos series que pueden darnos problemas en el proceso
distancias.dropna(inplace=True)

# Agrupamos por hospitales
distancias_clean = distancias.drop(
    columns=["geometry_nuc", "distance", "geometry_hospital", "CDTNUCLEO"]
)
distancias_clean.sort_values(by="CODIGO", ascending=True, inplace=True)

# Unimos las tablas asociando cada población a nucleo urbano y su hospital
hospitales_municipios_poblaciones = distancias_clean.merge(censo, on="CMUN")

# Select age group columns
age_columns = [
    "Total",
    "0 a 4",
    "5 a 9",
    "10 a 14",
    "15 a 19",
    "20 a 24",
    "25 a 29",
    "30 a 34",
    "35 a 39",
    "40 a 44",
    "45 a 49",
    "50 a 54",
    "55 a 59",
    "60 a 64",
    "65 a 69",
    "70 a 74",
    "75 a 79",
    "80 a 84",
    "85 a 89",
    "90 a 94",
    "95 a 99",
    "100 o más",
]

# Group by 'city' and sum the age group columns
hospital_population = (
    hospitales_municipios_poblaciones.groupby("CODIGO")[age_columns].sum().reset_index()
)

# Display the result
print(hospital_population)
