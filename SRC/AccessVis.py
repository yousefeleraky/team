import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium
import mapclassify
from pathlib import Path


class AccessViz:
    def __init__(self, travel_time_folder, travel_time_file):
        """
        Initialize AccessViz with folder and file name pattern to search for travel time data.

        Parameters:
        travel_time_folder (str): Folder name (or part of it) to locate travel time files.
        travel_time_file (list): List of filename patterns to search for.
        """
        self.travel_time_folder = travel_time_folder
        self.travel_time_file = travel_time_file
        self.grid = None

    def read_spatial_data(self):
        """
        Reads a spatial file (e.g., GeoJSON or shapefile) into a GeoDataFrame.

        Parameters:
        input_file (static path): Path to the spatial file.

        Returns:
        GeoDataFrame: The loaded spatial data.
        """
        try:
            self.grid = gpd.read_file('../data/MetropAccess_YKR_grid_EurefFIN.shp')
            return self.grid
        except Exception as e:
            print(f"Error reading spatial data: {e}")
            

    def file_finder(self):
        """
        Finds travel time files inside subfolders that match the given folder and filename patterns.

        Returns:
        list: List of matched file paths.
        """
        try:
            data_directory = Path('../data/travel_time_matrix')
            matched_files = []

            for folder in data_directory.rglob('*'):
                if self.travel_time_folder in folder.name:
                    for files in self.travel_time_file:
                        for file in folder.rglob('*'):
                            if str(files) in file.name:
                                matched_files.append(file)

            if not matched_files:
                print("No files matched the search criteria.")
            return matched_files
        except Exception as e:
            print(f"Error finding files: {e}")
            return []

    def convert_files_to_df(self, file_list):
        """
        Reads CSV files into DataFrames and merges them into one.

        Parameters:
        file_list (list): List of file paths to read.

        Returns:
        DataFrame: Concatenated DataFrame of all files.
        """
        try:
            df_list = []
            for file in file_list:
                df = pd.read_csv(file, sep=';')
                df_list.append(df)

            if not df_list:
                raise ValueError("No valid dataframes were loaded.")

            merged_lists = pd.concat(df_list, ignore_index=True)
            return merged_lists
        except Exception as e:
            print(f"Error converting files to DataFrame: {e}")
            return pd.DataFrame()

    def joining_table(self, right, output_path):
        """
        Joins the spatial layer with a DataFrame and saves to a file.

        Parameters:
        right (DataFrame): The DataFrame to join with the spatial data.
        output_path (str): Path to save the output spatial file.

        Returns:
        GeoDataFrame: The joined spatial layer.
        """
        try:
            if self.grid is None:
                raise ValueError("Spatial data is not loaded. Use read_spatial_data() first.")
            spatial_layer = self.grid.join(right)
            spatial_layer.to_file(f'{output_path}.shp')
            return spatial_layer
        except Exception as e:
            print(f"Error joining table or saving file: {e}")
            return None

    def interactive_map(self, spatial_layer, column,output_map_path):
        """
        Creates an interactive choropleth map using Folium.

        Parameters:
        spatial_layer (GeoDataFrame): Spatial layer to map.
        column (str): Column name to classify and visualize.

        Returns:
        folium.Map: Interactive map object.
        """
        try:
            classifier = mapclassify.NaturalBreaks(spatial_layer[column], k=9)
            spatial_layer["class"] = classifier.yb
            spatial_layer["id"] = spatial_layer.index.astype(str)

            m = folium.Map(location=(60.2, 25.0), zoom_start=12)

            folium.Choropleth(
                geo_data=spatial_layer,
                data=spatial_layer,
                columns=("id", "class"),
                key_on="feature.id",
                fill_color="YlOrRd",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="Travel Time Category"
            ).add_to(m)
            m.save(f'{output_map_path}.html')

            return m
        except Exception as e:
            print(f"Error generating interactive map: {e}")
            return None

    def staticmap(self, spatial_layer, column,output_map_path):
        """
        Displays a static map using matplotlib.

        Parameters:
        spatial_layer (GeoDataFrame): Spatial data.
        column (str): Column name to visualize.
        """
        try:
            spatial_layer.plot(
                column=column,
                scheme="quantiles",
                cmap="Spectral",
                linewidth=0,
                alpha=0.8
            )
            plt.title('Travel Time Category')
            plt.show()
            static=plt.savefig(f'{output_map_path}.png', dpi=300)
            return static
        except Exception as e:
            print(f"Error generating static map: {e}")

    def visualizer(self, inputuser, spatial_layer, column,output_map_path):
        """
        Visualizes the data either interactively or statically based on user choice.

        Parameters:
        inputuser (str): Either "interactive" or "static".
        spatial_layer (GeoDataFrame): Data to visualize.
        column (str): Column to visualize.

        Returns:
        Map or None: Folium map or static map depending on input.
        """
        try:
            if inputuser == 'interactive':
                return self.interactive_map(spatial_layer=spatial_layer, column=column,output_map_path=output_map_path)
            elif inputuser == 'static':
                return self.staticmap(spatial_layer=spatial_layer, column=column,output_map_path=output_map_path)
            else:
                raise ValueError('Choose between "static" or "interactive" only.')
        except Exception as e:
            print(f"Error in visualizer: {e}")
            return None
