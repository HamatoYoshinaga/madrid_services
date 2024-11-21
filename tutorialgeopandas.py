import geopandas
from geodatasets import get_path

path_to_data = get_path("nybb")
gdf = geopandas.read_file(path_to_data)

print(gdf)

gdf.to_file("tutorialgp/my_file.shp")

gdf = gdf.set_index("BoroName")
gdf["area"] = gdf.area

gdf.plot("area", legend=True)
