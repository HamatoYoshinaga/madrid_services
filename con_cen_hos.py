import geopandas as gpd

consultorios = gpd.read_file("input_data/DatosNmc/consultoriosalud.shp")
# consultorios = consultorios.drop(
#     columns=["TIPOVIA", "NOMVIA", "DESCR", "TIPON", "BUSCA", "NIF", "NUMERO", "CMUN",'MUNICIPIO','CD_VIAL']
# )
print(consultorios.columns)
# print(consultorios)
# print("########################################")
centros_salud = gpd.read_file("input_data/DatosNmc/centrosalud.shp")
print(centros_salud.columns)
# print("########################################")
hospitales = gpd.read_file("input_data/DatosNmc/hospital.shp")
print(hospitales.columns)
