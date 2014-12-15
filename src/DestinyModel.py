import json
import urllib

import DataParse
import DestinyGeometry

bungieUrlPrefix = "http://www.bungie.net"
bungieGeometryPrefix = "/common/destiny_content/geometry/platform/mobile/geometry/"

class DestinyModel(object):
    geometry = []
    def __init__(self, jsonFile):
        # Load the json file
        self.json = json.loads(jsonFile)
        
        print("Processing geometries...")
            
        # Get the geometry file names from the json and parse the geometries
        for geometryFile in self.json["content"][0]["geometry"]:
            path = bungieUrlPrefix+bungieGeometryPrefix+geometryFile
            print("Geometry file: "+path)
            response = urllib.request.urlopen(path)
            data = DataParse.DataParse(response.read())
            self.geometry.append(DestinyGeometry.parse(data))
        
        return