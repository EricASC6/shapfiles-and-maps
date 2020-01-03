import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os


class MapMaker:

    colors = {
        "buildings": "#664910",
        "landuse": "#2aba1a",
        "natural": "#7DF470",
        "railways": "#40403f",
        "roads": "#86b315",
        "waterways": "#007AF4"
    }

    def __init__(self, shape_files_dir):
        self.shape_files_dir = shape_files_dir

    def get_shape_files(self):
        city_maps = []
        for city in os.listdir(self.shape_files_dir):
            city_name = city[:-4]
            city_map_files = []
            city_path = os.path.join(self.shape_files_dir, city, "shape")
            for fil in os.listdir(city_path):
                file_name, ext = os.path.splitext(fil)
                if ext == ".shp" and file_name != "points" and file_name != "places":
                    city_map_files.append(fil)

            city_data = {
                "city_name": city_name,
                "city_map_files": sorted(city_map_files, reverse=True),
                "city_path": city_path
            }

            print(city_data)
            city_maps.append(city_data)

        return city_maps

    def concat_shape_files(self, city_maps):
        maps = []
        for city_data in city_maps:
            gdf_objects = []
            for map_file in city_data["city_map_files"]:
                path = os.path.join(city_data["city_path"], map_file)
                loc, _ = city_loc = os.path.splitext(map_file)
                gdf = gpd.read_file(path)

                # filtering the important stuff
                if map_file == "roads.shp":
                    gdf = gdf.loc[gdf["type"] == "primary"]
                elif map_file == "buildings.shp":
                    gdf = gdf.loc[gdf["type"] == "residential"]
                elif map_file == "natural.shp":
                    gdf = gdf.loc[gdf["type"] == "water"]
                gdf["color"] = [MapMaker.colors[loc] for i in gdf["osm_id"]]
                gdf_objects.append(gdf)
            concat_map = pd.concat(gdf_objects, sort=True)
            concat_gdf = gpd.GeoDataFrame(concat_map)
            final_city_map = {
                "name": city_data["city_name"],
                "map": concat_gdf
            }
            maps.append(final_city_map)

        return maps

    def plot_maps(self, maps):
        for _map in maps:
            _map["map"].plot(color=_map["map"]["color"])
            plt.savefig(os.path.join("./images", _map["name"] + ".png"))
