import pandas as pd

# Cargar los datos
hospitales_df = pd.read_csv(
    "qgis_files/hospitales_zonasalud.csv"
)  # Resultado de la intersección en QGIS
centrosalud_df = pd.read_csv(
    "output_data/centros_salud.csv"
)  # Hospital más cercano por municipio

# Asegurarse de que los códigos estén en el mismo formato
hospitales_df["CDTDISTSAL"] = hospitales_df["CDTDISTSAL"].astype(int)
centrosalud_df["CODDISTR"] = centrosalud_df["CODDISTR"].astype(int)

# Seleccionar solo las columnas necesarias
hospitales_reducido = hospitales_df[["CDTDISTSAL", "ETIQUETA"]]
centros_salud_reducido = centrosalud_df[["CODDISTR", "ETIQUETA"]]

# Realizar la unión por 'CDTDISTSAL' en hospitales y 'CODDISTR' en centros de salud
resultado_df = pd.merge(
    centros_salud_reducido,
    hospitales_reducido,
    left_on="CODDISTR",
    right_on="CDTDISTSAL",
    how="left",
)

# Guardar el resultado en un nuevo CSV
resultado_df.to_csv("output_data/centros_y_hospitales.csv", index=False)


print("Asignación de hospitales completada.")
