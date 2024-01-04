import os
import requests
from BungieDatabase import BungieDatabase 

## CONFIGURE - add API key between single quotes below ##
apikey = '' # You can generate an API key at https://www.bungie.net/en/Application
###############

outputPath = "../stl"

def main():
    global apikey
    print("Welcome to the Destiny stl generator")

    if apikey == '':
        uinput = input("You have not provided an API key.\nEither add your API key to main.py or enter it here: ")
        apikey = uinput

    s = requests.session()
    s.headers = {
        'X-API-Key': apikey
    }
    
    # Create a Bungie Database object and connect to it
    db = BungieDatabase(s)
    db.connect()
    
    if not os.path.exists(outputPath):
        print("Creating stl output directory "+outputPath)
        os.makedirs(outputPath)
        
    while True:
        # Get user request
        command = input("Enter an item name or id: ")
        
        # Break if q, quit or exit was typed
        if command == "q" or command == "quit" or command == "exit":
            break
        # Update the database if requested
        elif command == "update":
            db.update()
        # Assume the entered text was an item name or id
        else:
            # Download the model data for this item
            item = command
            model = db.getModel(item)
            
            # If the model is not null generate the stl file
            if model is not None:
                model.generate(outputPath+"/"+item+".stl")
    
    # Close the database and exit
    db.close()
    print("Bye.")
    exit()

if __name__ == '__main__':
    main()
