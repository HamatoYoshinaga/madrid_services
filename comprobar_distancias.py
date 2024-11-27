import pandas as pd
import numpy as np

# Leer csv, este csv viene con datos de todos los años desde 1996
# y con datos sobre la población masculina y femenina. Por eso lo filtramos
output_df = pd.read_csv(
    "output_data/distancias_nuc_hos.csv",
    delimiter=",",
    engine="python",
)

distancias_minimas = pd.read_csv(
    "input_data/distancias_minimas_hospitales.csv", delimiter=",", engine="python"
)
tiempos_minimos = pd.read_csv(
    "input_data/tiempos_minimos_hospitales.csv", delimiter=",", engine="python"
)

# Initialize an empty list to store results
distancias_no_coinciden = np.array([])
tiempos_no_coinciden = np.array([])

# Iterate through the rows of df1
for _, row in distancias_minimas.iterrows():
    geocodigo = row["geocodigo"]
    codigo = row["codigo"]
    distancias_obtenidas = output_df[output_df["CDTNUCLEO"] == geocodigo]
    if distancias_obtenidas[distancias_obtenidas["CODIGO"] == codigo].empty:
        distancias_no_coinciden = np.append(distancias_no_coinciden, geocodigo)

# Iterate through the rows of df2
for _, row in tiempos_minimos.iterrows():
    geocodigo = row["geocodigo"]
    codigo = row["codigo"]
    distancias_obtenidas = output_df[output_df["CDTNUCLEO"] == geocodigo]
    if distancias_obtenidas[distancias_obtenidas["CODIGO"] == codigo].empty:
        tiempos_no_coinciden = np.append(tiempos_no_coinciden, geocodigo)

# Check for common elements
common_elements = np.intersect1d(distancias_no_coinciden, tiempos_no_coinciden)
print(common_elements)

# Check if any common elements exist
todo_coincide = distancias_no_coinciden.size == 0 & tiempos_no_coinciden.size == 0
has_common = common_elements.size > 0
if has_common:
    print("algunos valores no coinciden")
elif todo_coincide:
    print("las distancias calculadas coinciden con los tiempos y distancias minimas")
else:
    print(
        "almenos la distancia o el tiempo minimo coinciden con las distancias calculadas"
    )
