import io
import json
import struct
import os
#import urllib.request
import requests
import zipfile
import sqlite3

import DestinyModel

bungieUrlPrefix = "http://www.bungie.net"
destinyManifestUrl = "http://www.bungie.net/platform/Destiny2/Manifest/"
myDbFile = "./database/gear.db"

class BungieDatabase(object):
    def __init__(self,requests_session):
        self.s = requests_session
        # Set file path if database already exists
        if os.path.isfile(myDbFile):
            self.filePath = myDbFile
        else:
            # Create database
            self.update()
        return
        
    def update(self):
        if os.path.isfile(myDbFile):
            print("Deleting old gear database...")
            os.remove(myDbFile)
            
        if not os.path.exists("./database"):
            print("Creating database directory...")
            os.makedirs("./database")
            
        # Open the Destiny manifest from bungie.net and load it as json
        print("Downloading gear database from bungie.net...")
        #response = urllib.request.urlopen(destinyManifestUrl)
        #manifest = json.loads(response.read().decode())
        response = s.get(destinyManifestUrl)
        manifest = response.json()
        
        # Read the path for the gear database file and open it
        path = bungieUrlPrefix+manifest["Response"]["mobileGearAssetDataBases"][2]["path"]
        #response = urllib.request.urlopen(path)
        response = s.get(path)

        # Gunzip the database file
        #gearZip = zipfile.ZipFile(io.BytesIO(response.read()))
        # zipNameList = gearZip.namelist()
        # for filename in zipNameList:
        #     if "asset_sql_content" in filename:
        #         gearZip.extract(filename)
        #         bungieDbFile = filename

        gearZip = zipfile.ZipFile(io.BytesIO(response.content))
        zipNameList = gearZip.namelist()
        for filename in zipNameList:
            if "asset_sql_content" in filename:
                gearZip.extract(filename)
                bungieDbFile = filename
        
        # Create out own gear database
        print("Creating new gear database...")
        conn = sqlite3.connect(myDbFile)
        c = conn.cursor()
        c.execute("CREATE TABLE gear (id INT, name TEXT, json INT)")
        
        print("Updating the gear database...")
        print("This will take a few minutes...")
        
        # Open the database and get a cursor object
        connBungie = sqlite3.connect(bungieDbFile)
        cBungie = connBungie.cursor()
        
        # Get the names for all items
        #cBungie.execute("SELECT id, json FROM DestinyGearAssetsDefinition")
        cBungie.execute("SELECT CASE WHEN id < 0 THEN id + 4294967296 ELSE id END AS id, json FROM DestinyGearAssetsDefinition")
        for row in cBungie:
            #itemId = struct.unpack('L', struct.pack('l', row[0]))[0]
            itemId = row[0]
            itemJson = row[1]
            # print(itemJson)
            try:
                # response = urllib.request.urlopen(destinyManifestUrl+"inventoryItem/"+str(itemId))
                # itemManifest = json.loads(response.read().decode())
                response = s.get(destinyManifestUrl+"DestinyInventoryItemDefinition/"+str(itemId))
                # print(response.request.url)
                # print(response.text)
                # print(response.status_code)
                itemManifest = response.json()
                #itemName = itemManifest["Response"]["data"]["inventoryItem"]["itemName"].replace('"',"").rstrip()
                itemName = itemManifest["Response"]["displayProperties"]["name"]
                print("Adding "+itemName+" from: "+destinyManifestUrl+"inventoryItem/"+str(itemId))
                c.execute("INSERT INTO gear VALUES (?,?,?)", (itemId, itemName, itemJson))
            except Exception as e:
                # Skip this entry
                print(str(e))
                print("Skipping item id",itemId,"...")
                continue
        
        print("Done updating the gear database...")# save (commit) the changes
        conn.commit()
        conn.close()
        connBungie.close()
        
        print("Cleaning up temp files...")
        os.remove(bungieDbFile)
        
        self.filePath = myDbFile
        
        return
    
    def connect(self):
        # Open the database and get a cursor object
        print("Connecting to gear database...")
        self.db = sqlite3.connect(self.filePath)
        self.cursor = self.db.cursor()
        
        return
    
    def getModel(self, item):
        # Assume the item 
        self.cursor.execute('''SELECT json FROM gear WHERE name=? COLLATE NOCASE''', (item,))
        response = self.cursor.fetchone()
        if response is None:
            try:
                # Convert id string to unsigned int
                item = int(item)
            except:
                print("Unable to find item "+item+" please try again...")
                return
                
            self.cursor.execute('''SELECT json FROM gear WHERE id=?''', (item,))
            response = self.cursor.fetchone()
            if response is None:
                print("Unable to find item "+str(item)+" please try again...")
                return

        # Return the model defined by the json file
        return DestinyModel.DestinyModel(response[0],self.s)
    
    def close(self):
        # Close the gear database
        print("Closing the gear database...")
        self.db.close()
        
        return