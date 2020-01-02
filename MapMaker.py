import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os


class MapMaker:

    colors = {
        "buildings": "#B5B5B5",
        "landuse": "#30CA1F",
        "natural": "#7DF470",
        "places": "#009DBC",
        "points": "#DFF01D",
        "railways": "#BA7701",
        "roads": "#EAEAEA",
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
                if os.path.splitext(fil)[1] == ".shp":
                    city_map_files.append(fil)

            city_data = {
                "city_name": city_name,
                "city_map_files": city_map_files,
                "city_path": city_path
            }

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
                gdf["color"] = [MapMaker.colors[loc]
                                for i in gdf["osm_id"]]
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
