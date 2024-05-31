from typing import Optional
from Model.Entities import Pokemon, Trainer
from Model.DB_Interface import DB_Interface

class Pokemon_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db

    def add(self, new_pokemon: Pokemon) -> Pokemon:
        self.db.add_new_pokemon(new_pokemon)
        return new_pokemon
    
    def get_by_id(self, id: int) -> Pokemon:
        return self.db.get_pokemon_by_id(id)
    
    def get_by_trainer_id(self, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_trainer_id(trainer_id)
    
    def get_by_type(self, type: str) -> list[dict]:
        return self.db.get_pokemons_by_type(type)
    
    def get_by_type_and_trainer_id(self, type: str, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_type_and_trainer_id(type, trainer_id)
    

class Trainer_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db

    def get_all(self) -> list[Trainer]:
        return []
    
    def get_by_pokemon_id(self, pokemon_id: int) -> Optional[list[Trainer]]:
        return self.db.get_trainers_by_pokemon_id(pokemon_id)