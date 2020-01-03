from MapMaker import MapMaker


def main():
    try:
        shape_files_path = "./shapefiles"
        map_maker = MapMaker(shape_files_path)
        shapefiles = map_maker.get_shape_files()
        merged = map_maker.concat_shape_files(shapefiles)
        map_maker.plot_maps(merged)
    except:
        print("Something went wrong")


if __name__ == "__main__":
    main()
