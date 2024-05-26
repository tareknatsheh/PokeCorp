class Database:
    def __init__(self):
        print("Initializing the DB")
        pass

    def findByType(self, type: str) -> list[str]:
        return []
    
    def findOwners(self, pokemon_name: str) -> list[str]:
        return []
    
    def findPokemonsOfOwner(self, owner_name) -> list[str]:
        return []


db = Database()