from graph_requests import Graph 
import json 
import asyncio 
with open("config.json", "r") as config_file:
    ms = Graph(config_file.read())
    config_file.seek(0)
    settings = json.loads(config_file.read())
    shared_lib = settings["sharedLibrary"]
hospice = "01DMUEVTWDBTLYMWPP5JFYRHN7ICOVTF6J"
volunteers = "01DMUEVTVRFBV7MNDVEVCK47PLJ5ZUNY2F"
result = asyncio.run(ms.search_file(parent_id=volunteers, drive_id=shared_lib,file_name="Volunteer Flu Declination Forms"))

print(f"Result: {result}")