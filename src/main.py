import os
from BungieDatabase import BungieDatabase 

outputPath = "../stl"

def main():
    print("Welcome to the Destiny stl generator")
    
    # Create a Bungie Database object and connect to it
    db = BungieDatabase()
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
