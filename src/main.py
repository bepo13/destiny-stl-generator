from BungieDatabase import BungieDatabase 

def main():
    # Create a Bungie Database object and connect to it
    db = BungieDatabase()
    db.connect()
    
#     model = db.getModel(144553854)
#     model.generate("../stl/achlyophage_symbiote.stl")

    model = db.getModel(346443849)
    model.generate("../stl/mythoclast.stl")
    
#     model = db.getModel(3458901841)
#     model.generate("../stl/light_in_the_abyss.stl")
    
#     model = db.getModel(845577225)
#     model.generate("../stl/s13_graverobber.stl")
    
    # Close the database and exit
    db.close()
    print("Done")
    exit()

if __name__ == '__main__':
    main()
