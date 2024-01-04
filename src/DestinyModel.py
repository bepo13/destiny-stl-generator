import os
import json
import requests

import DataParse
import DestinyGeometry

bungieUrlPrefix = "http://www.bungie.net"
#bungieGeometryPrefix = "/common/destiny_content/geometry/platform/mobile/geometry/"
bungieGeometryPrefix = "/common/destiny2_content/geometry/platform/mobile/geometry/"

class DestinyModel(object):
    def __init__(self, jsonFile,requests_session):
        self.s = requests_session
        self.geometry = []
        
        # Load the json file
        self.json = json.loads(jsonFile)
        
        print("Processing geometries...")
            
        # Get the geometry file names from the json and parse the geometries
        for geometryFile in self.json["content"][0]["geometry"]:
            path = bungieUrlPrefix+bungieGeometryPrefix+geometryFile
            print("Geometry file: "+path)
            response = self.s.get(path)
            data = DataParse.DataParse(response.content)
            self.geometry.append(DestinyGeometry.parse(data))
        
        return
    
    def generate(self, fileName):
        #Open file
        with open(fileName, 'w') as fo:
            print("Writing "+fileName+"...")
                      
            # Write name header
            fo.write("solid temp\n")
             
            # Generate stl data for each geometry
            for geometry in self.geometry:
                status = geometry.generate(fo)
                if status == False:
                    # Something went wrong, cleanup the file and return
                    fo.close()
                    os.remove(fileName)
        
            # Success, close the file and return
            print("Finished writing "+fileName+"!")
            fo.close()
            
        return
    