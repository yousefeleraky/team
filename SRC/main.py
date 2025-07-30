from fastapi import FastAPI, UploadFile,HTTPException
from typing import List
from utility import AccessViz
from pydantic import BaseModel



app = FastAPI()
class visualizationInput(BaseModel):
    folder: str 
    file: str
    column: str 
    map_type: str 
    output_layer_name: str
    output_map_name:str

@app.post('/visualization_tool')
async def visualization_tool(
    
    
    inputs:visualizationInput
    
    
):
 """this is visualization tool that convert tablur data to geodataframe
 params:-
 
 folder: is the folder name that contain files
 
 file: is the folder name that contain travel time data
 
 column: is the travel mode type that you want to visualize 
 
 map_type: is the type of the map choose between(static,interactive)
 
 output_layer_path : the output of the result as shapefile
 
 output_map_path the out put that you want to save the map at it"""
 
 
 if inputs.folder is None or inputs.file is None:
     raise ValueError('please insert valid file number or folder')
 try:
   study_area=AccessViz(inputs.folder,inputs.file)
   
   grid=study_area.read_spatial_data()
   travel_time_files=study_area.file_finder()
   if travel_time_files is None:
       raise ValueError('there is no file has matched')
   merged_file=study_area.convert_files_to_df(travel_time_files)
   grid_with_travel_time_values=study_area.joining_table(merged_file,output_path=inputs.output_layer_name)
   map_layer=study_area.visualizer(inputuser=inputs.map_type,spatial_layer=grid_with_travel_time_values,column=inputs.column,output_map_path=inputs.output_map_name)
   if map_layer is None:
       raise ValueError('the map layer is empty try valid data')     
   return {"message": "Map saved successfully", "output_map_path": inputs.output_map_name}
 
 except Exception as e:
     raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

   
