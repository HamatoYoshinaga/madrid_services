import pandas as pd

distancias = pd.read_csv("output_data/distancia_min_nuc_hos.csv")

# Borramos series que pueden darnos problemas en el proceso
distancias = distancias.dropna()

# Agrupamos por hospitales
distancias_clean = distancias.drop(
    columns=["geometry_nuc", "distance", "geometry_hospital", "CDTNUCLEO"]
)
distancias_clean.sort_values(by="CODIGO", ascending=True, inplace=True)
print(distancias_clean)
