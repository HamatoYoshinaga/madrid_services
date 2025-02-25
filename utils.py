import pandas as pd


def filtrar_centros_sin_hospital(ruta_csv):
    """
    Carga un archivo CSV y devuelve un DataFrame con los centros de salud
    que no tienen un hospital asociado (vacío o 'No encontrado').

    :param ruta_csv: Ruta del archivo CSV.
    :return: DataFrame filtrado.
    """
    # Cargar el CSV sin encabezados
    df = pd.read_csv(ruta_csv, header=None)

    # Asignar nombres de columna
    df.columns = ["CODDISTR", "Centro de Salud", "Código", "Hospital Asociado"]

    # Filtrar los centros de salud sin hospital asociado (NaN o 'No encontrado')
    df_sin_hospital = df[df["Hospital Asociado"].isna()]

    df_sin_hospital = df_sin_hospital.drop(columns=["Código", "Hospital Asociado"])

    return df_sin_hospital


def filtrar_consultorios_sin_centros(ruta_csv):
    """
    Carga un archivo CSV y devuelve un DataFrame con los centros de salud
    que no tienen un hospital asociado (vacío o 'No encontrado').

    :param ruta_csv: Ruta del archivo CSV.
    :return: DataFrame filtrado.
    """
    # Cargar el CSV sin encabezados
    df = pd.read_csv(ruta_csv, header=None)

    # Asignar nombres de columna
    df.columns = ["consultorio", "web", "Código", "Hospital Asociado"]

    # Filtrar los centros de salud sin hospital asociado (NaN o 'No encontrado')
    df_sin_centro = df[(df["Hospital Asociado"] == "No encontrado")]

    df_sin_centro = df_sin_centro.drop(columns=["Código", "Hospital Asociado"])

    return df_sin_centro


# (Opcional) Guardar el resultado en un nuevo CSV
df_sin_hospital = filtrar_centros_sin_hospital("output_data/centros_y_hospitales.csv")
df_sin_hospital.to_csv("datos_a_enviar/centros_sin_hospital.csv", index=False)
df_sin_centro = filtrar_consultorios_sin_centros(
    "output_data/consultorios_centros_salud.csv"
)
df_sin_centro.to_csv("datos_a_enviar/consultorios_sin_centro.csv", index=False)
