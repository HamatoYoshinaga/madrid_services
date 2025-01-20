import geopandas as gpd

municipios = gpd.read_file("input_data/DatosNmc/muni2023.shp")
municipios.to_csv("output_data/municipios.csv")
print("File saved to output_data/municipios.csv")

# nucleourbano = gpd.read_file("input_data/DatosNmc/nucl2023.shp")
# nucleourbano.to_csv("output_data/nucleosurbanos.csv")
# print("File saved to output_data/nucleosurbanos.csv")

# consultorios = gpd.read_file("input_data/DatosNmc/consultoriosalud.shp")
# link_consultorios = consultorios[["ETIQUETA", "URL"]]
# link_consultorios.to_csv("output_data//link_consultorios.csv", index=False)
# output_path = "output_data/consultorios.csv"
# consultorios.to_csv(output_path, index=False)
# print(f"output saved to {output_path}")

# centros_salud = gpd.read_file("input_data/DatosNmc/centrosalud.shp")
# output_path = "output_data/centros_salud.csv"
# centros_salud.to_csv(output_path, index=False)
# print(f"output saved to {output_path}")

# hospitales = gpd.read_file("input_data/DatosNmc/hospital.shp")
# output_path = "output_data/hospitales.csv"
# hospitales.to_csv(output_path, index=False)
# print(f"output saved to {output_path}")

# zonasalud = gpd.read_file("input_data/DatosNmc/zonasaludunica.shp")
# zonasalud = zonasalud.drop(columns=["geometry"])
# output_path = "output_data/zonasalud.csv"
# zonasalud.to_csv(output_path, index=False)
# print(f"output saved to {output_path}")
