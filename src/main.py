import BungieDatabase

def main():
    # Create a Bungie Database object and connect to it
    database = BungieDatabase.BungieDatabase()
    database.connect()
    
    # Get the geometry model for Achlyophage Symbiote
#     database.getModel(144553854)
    model = database.getModel(346443849)
    
    # Close the database and exit
    database.close()
    print("Done")
    exit()

if __name__ == '__main__':
    main()
