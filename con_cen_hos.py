import geopandas as gpd

consultorios = gpd.read_file("input_data/DatosNmc/consultoriosalud.shp")
output_path = "output_data/consultorios.csv"
consultorios.to_csv(output_path, index=False)
print(f"output saved to {output_path}")

centros_salud = gpd.read_file("input_data/DatosNmc/centrosalud.shp")
output_path = "output_data/centros_salud.csv"
centros_salud.to_csv(output_path, index=False)
print(f"output saved to {output_path}")

hospitales = gpd.read_file("input_data/DatosNmc/hospital.shp")
output_path = "output_data/hospitales.csv"
hospitales.to_csv(output_path, index=False)
print(f"output saved to {output_path}")

zonasalud = gpd.read_file("input_data/DatosNmc/zonasaludunica.shp")
zonasalud = zonasalud.drop(columns=["geometry"])
output_path = "output_data/zonasalud.csv"
zonasalud.to_csv(output_path, index=False)
print(f"output saved to {output_path}")
