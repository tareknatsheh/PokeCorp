from Model.Entities import Pokemon
from Model.mysql_repo import MySql_repo as repo
from typing import Optional

class Database:
    def __init__(self):
        self.my_db = repo()
        pass
    
    # -------- Pokemon -----------
    # done
    def find_pokemon_by_id(self, id: int) -> Pokemon | None:
        try:
            return self.my_db.get_pokemon_by_id(id)
        except Exception as e:
            print(f"Error: find_by_id: {e}")
            raise
    
    # TODO
    def find_pokemon_by_type(self, type: str) -> list[dict]:
        return self.my_db.find_pokemon_by_type(type)
    
    # done
    def find_pokemons_by_trainer_id(self, trainer_name) -> list[dict]:
        return self.my_db.find_pokemons_by_trainer_id(trainer_name)
    
    def find_pokemons_by_type_and_trainer_id(self, type, trainer_name):
        return self.my_db.find_pokemons_by_type_and_trainer_id(type, trainer_name)
    
    # done
    def add_new_pokemon(self, new_pok: Pokemon):
        try:
            return self.my_db.add_new_pokemon(new_pok)
        except Exception as e:
            print(f"Error: add_new_pokemon: {e}")
            raise
    
    # -------- Trainer -----------
    def find_trainers_by_pokemon_id(self, pokemon_id: int):
        return self.my_db.find_trainers_by_pokemon_id(pokemon_id)
    
    def find_all_trainers(self):
        return self.my_db.find_all_trainers()



db = Database()