from Model.Entities import Pokemon
from Model.Pokemon_DB_Interface import Pokemon_DB_Interface

class Pokemon_Repo:
    def __init__(self, db: Pokemon_DB_Interface):
        self.db = db

    def add(self, new_pokemon: Pokemon) -> Pokemon:
        self.db.add_new_pokemon(new_pokemon)
        return new_pokemon
    
    def get_by_id(self, id: int) -> Pokemon:
        return self.db.get_pokemon_by_id(id)
    
    def get_by_trainer_id(self, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_trainer_id(trainer_id)
    
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        return self.db.get_pokemons_by_type(type)
    
    def get_pokemons_by_type_and_trainer_id(self, type: str, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_type_and_trainer_id(type, trainer_id)
    

        # if not self.cursor:
        #     raise Exception("cursor not initialized")
        
        # self.cursor.execute(query, (type,))
        # result = self.cursor.fetchall()
        # result = [{"id": p[0], "name": p[1], "height": p[2], "weight": p[3]} for p in result]
        # return result