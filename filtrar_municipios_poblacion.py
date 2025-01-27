import pandas as pd

df = pd.read_csv(
    "input_data/censoCM_INE.csv",
    delimiter=";",
    engine="python",
)

# Filtrar por población Total y periodo más actual
df = df[df["Sexo"] == "Total"]
df = df[df["Periodo"] == 2023]
df = df[["Municipios", "Total"]]

# Corregir formato
df["CMUN28"] = df["Municipios"].str.extract(r"(\d+)").astype(int)
df["CMUN"] = df["CMUN28"] % 1000

df.rename(columns={"Total": "poblacion"}, inplace=True)
df["poblacion"] = df["poblacion"].apply(lambda x: int(x.replace(".", "")))
df = df[["poblacion", "CMUN"]]

resultado_df = df[df["poblacion"] <= 50000]
# Guardar el resultado en un nuevo CSV
resultado_df.to_csv("output_data/municipios_s.csv", index=False)

print("Municipios filtrados guardados a 'output_data/municipios_s.csv'.")
