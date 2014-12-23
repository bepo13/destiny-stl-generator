import io
import json
import struct
import os
import os.path
import urllib.request
import zipfile
import sqlite3

import DestinyModel

bungieUrlPrefix = "http://www.bungie.net"
destinyManifestUrl = "http://www.bungie.net/platform/Destiny/Manifest/"
databaseFile = "gear.db"

class BungieDatabase(object):
    def __init__(self):
        # Set file path if database already exists
        if os.path.isfile(databaseFile):
            self.filePath = databaseFile
        else:
            # Create database
            self.update()
        return
        
    def update(self):
        # Open the Destiny manifest from bungie.net and load it as json
        response = urllib.request.urlopen(destinyManifestUrl)
        self.manifest = json.loads(response.read().decode())
        
        print("Updating destiny gear database with latest definitions...")
        
        # Read the path for the gear database file and open it
        path = bungieUrlPrefix+self.manifest["Response"]["mobileGearAssetDataBases"][1]["path"]
        response = urllib.request.urlopen(path)

        # Gunzip the database file
        gearZip = zipfile.ZipFile(io.BytesIO(response.read()))
        zipNameList = gearZip.namelist()
        for filename in zipNameList:
            if "asset_sql_content" in filename:
                gearZip.extract(filename)
                os.rename(filename, databaseFile)
                self.filePath = databaseFile
        
#         # Add names to all items
#         self.cursor.execute("SELECT id FROM DestinyGearAssetsDefinition")
#         deleteList = []
#         for row in self.cursor:
#             try:
#                 itemId = row[0]
#                 if itemId < 0:
#                     itemId = struct.unpack('L', struct.pack('l', itemId))[0]
#                 response = urllib.request.urlopen(destinyManifestUrl+"inventoryItem/"+str(itemId))
#                 itemManifest = json.loads(response.read().decode())
#                 print(destinyManifestUrl+"inventoryItem/"+str(itemId))
#                 print(itemManifest["Response"]["data"]["inventoryItem"]["itemName"])
#             except:
#                 # Remove this entry from the DB
#                 deleteList.append(row)
#                 
#         for row in deleteList:
#             print("Removing entry",row[0],"from the database...")
#             self.cursor.execute("DELETE FROM DestinyGearAssetsDefinition WHERE id=?", row)
#             
#         # Add all item names to the database
#         self.cursor.execute("alter table DestinyGearAssetsDefinition add column name string")

        return
    
    def connect(self):
        # Open the database and get a cursor object
        self.db = sqlite3.connect(self.filePath)
        self.cursor = self.db.cursor()
        
        return
    
    def getModel(self, itemId):
        # Convert unsigned item id to signed id
        if itemId > 2147483647:
            itemId = struct.unpack('l', struct.pack('L', itemId))[0]
            
        # Fetch the JSON file for this item ID and create the model
        self.cursor.execute('''SELECT json FROM DestinyGearAssetsDefinition WHERE id=?''', (itemId,))
        jsonData = self.cursor.fetchone()[0]
        return DestinyModel.DestinyModel(jsonData)
            
        return
    
    def close(self):
        # Close the gear database
        self.db.close()
        
        return