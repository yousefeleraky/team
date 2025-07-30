# AccessViz

## overview
AccessViz project is a wep api built with fastapi that transform tabular travel time data into:
1. **static**: using matplotlib library to visualize the data on the map 
2. **interactive**: using folium library to make interactive html wep map 

## Structure
```plaintext
/team
├──DATA/
|     ├──travel_time_matrix.zip
| 
├──DEP/
|    ├──Requirements.txt
|
├──DOC/
|    ├──API Documentation.md
|    ├──Postman_collection
|
├──SRC/
|     ├──main.py
|     ├──AccessVis.py
|
├──README.md


```

## installation
Install the required dependencies:
git clone https://github.com/yousefeleraky/team.git
cd team
pip install -r Requirements.txt

## Usage

To run the API locally:
 
uvicorn main:app --reload

Once the server is running, you can use a tool like Postman or `curl` to make requests to the API.

## features

Read and process spatial grid data.
Automatically locate and merge travel time files.
Join tabular data with spatial data to produce GeoDataFrames.
Create either interactive (HTML) or static (image) maps.
Export the spatial layer as a Shapefile.
Save the generated map to a specified output path

## requirements
check the requirements text





### Example Request for AccessViz
**Endpoint**: `post/ visualization_tool`
 
Request Body:
```json
{
  
  "folder": "578",
  "file": "57840",
  "column": "car_m_d",
  "map_type": "interactive",
  "output_layer_name": "travel_map",
  "output_map_name": "travel_map"

}
```
example response
```json
{
  "message": "Map saved successfully",
  "output_map_path": "outputs/travel_map.html"
}
```
## on error
```json
{
  "detail": "Analysis error: the map layer is empty try valid data"
}
```
## dependencies
- `pandas`: to read tabular data and convert it into data frame
- `geopandas`: to read spatial data and do spatial analysis
- `folium`: make interactive wep map
- `matplotlib`: make static map using ploting
- `mapclassify`: normalize data into classes to help you in visualization
- `pathlib`: locate files on your machine
- `fastapi`: for making endpoint
- `uvicorn`: run the code on your local machine