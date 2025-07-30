# visualization_tool
this API provides functionality to reacive travel time matrix texts to visualize data on spatial layer
and show it on a map using matplotlib if you want static map
or folium if you want interactive web map 

---

### **POST**  `/visualization_tool`
**Description**: recieve file and folder name and return visual map and shapefile layer 

### **Request body parameters**: 
Parameter  | Type | Description

`folder`  | String | contain folder name
`file` | String | contain traveltime file name
`column`  | String | contain column name that you want to visualize on the map
`map_type`  | String | contain map type choose between (static/interactive)
`outputlayer_name`  | String | contain layer name without file format
`output_map_name`  | String | contain map name without file format


#### **Response**:
- **Success** (200):

```json
{
  "message": "Map saved successfully",
  "output_map_path": "outputs/travel_map.html"
}
```
- **Error** (500):
```json
{
  "detail": "Analysis error: the map layer is empty try valid data"
}
```

## Request Example 

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
## Response Example


```json
{
  "message": "Map saved successfully",
  "output_map_path": "outputs/travel_map.html"
}
```

**the output should be file contain the map and shapefile contain the spatial layer**