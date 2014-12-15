import io
import json
import urllib.request
import zipfile
import sqlite3

import DestinyModel

bungieUrlPrefix = "http://www.bungie.net"
bungieGeometryPrefix = "/common/destiny_content/geometry/platform/mobile/geometry/"
destinyManifestUrl = "/platform/Destiny/Manifest/"

class BungieDatabase(object):
    def __init__(self):
        # Open the Destiny manifest from bungie.net and load it as json
        response = urllib.request.urlopen(bungieUrlPrefix+destinyManifestUrl)
        self.manifest = json.loads(response.read().decode())
        
        print("Opening destiny gear database...")
        
        # Read the path for the gear database file and open it
        path = bungieUrlPrefix+self.manifest["Response"]["mobileGearAssetDataBases"][1]["path"]
        response = urllib.request.urlopen(path)

        # Gunzip the database file
        gearZip = zipfile.ZipFile(io.BytesIO(response.read()))
        zipNameList = gearZip.namelist()
        for filename in zipNameList:
            if "asset_sql_content" in filename:
                gearZip.extract(filename, 'temp')
                self.filePath = 'temp/'+filename
        if self.filePath == None:
            print("Unable top open asset_sql_content file, exiting...")
            exit()
            
        return
    
    def connect(self):
        # Open the database and get a cursor object
        self.db = sqlite3.connect(self.filePath)
        self.cursor = self.db.cursor()
        
        return
    
    def getModel(self, itemId):
        # Fetch the JSON file for this item ID and create the model
        self.cursor.execute('''SELECT json FROM DestinyGearAssetsDefinition WHERE id=?''', (itemId,))
        jsonData = self.cursor.fetchone()[0]
        return DestinyModel.DestinyModel(jsonData)
            
        return
    
    def close(self):
        # Close the gear database
        self.db.close()
        
        return