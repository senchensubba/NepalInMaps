import geopandas as gpd
import pandas as pd
from pathlib import Path

class WardPopulationMerger:
    def __init__(self, geojson_path, csv_path):
        self.geojson_path = geojson_path
        self.csv_path = csv_path
        self.wards_gdf = None
        self.population_df = None
        self.merged_gdf = None

    def load_data(self):
        self.wards_gdf = gpd.read_file(self.geojson_path)
        self.population_df = pd.read_csv(self.csv_path)

    def inspect_columns(self):
        print("GeoJSON columns:", self.wards_gdf.columns.tolist())
        print("CSV columns:", self.population_df.columns.tolist())

    def merge_data(self, geojson_keys, csv_keys):
        self.merged_gdf = self.wards_gdf.merge(
            self.population_df,
            left_on=geojson_keys,
            right_on=csv_keys,
            how="inner"
        )
        return self.merged_gdf

    def save_merged(self, output_path):
        if self.merged_gdf is not None:
            self.merged_gdf.to_file(output_path, driver="GeoJSON")
            print(f"Merged file saved to: {output_path}")
        else:
            print("No merged data found.")


# ---- Example Usage ----
if __name__ == "__main__":
    geojson_path = Path("data/external/geojson-nepal/nepal-wards.geojson")
    csv_path = Path("data/raw/ward_population_density_2021.csv")
    output_path = Path("data/processed/wards_with_population.geojson")

    merger = WardPopulationMerger(geojson_path, csv_path)
    merger.load_data()
    merger.inspect_columns()  # You check output here, then set merge keys
