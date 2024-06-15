from typing import Optional
from fastapi import HTTPException, status
from Model.Entities import Pokemon, Trainer
from Model.DB_Interface import DB_Interface

class Pokemon_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db
    
    def add(self, pokemon_id: int) -> dict:
        return self.db.add_new_pokemon(pokemon_id)
    
    def get_by_trainer_id(self, trainer_id: int) -> list[dict]:
        return self.db.get_pokemons_by_trainer_id(trainer_id)
    
    def get_by_type(self, type: str) -> list[dict]:
        return self.db.get_pokemons_by_type(type)
    

class Trainer_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db
    
    def get_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        return self.db.get_trainers_by_pokemon_id(pokemon_id)
    
    def delete_a_pokemon(self, trainer_id: int, pokemon_id: int) -> Optional[int]:
        return self.db.delete_pokemon_of_trainer(trainer_id, pokemon_id)
    
    def add_new_pokemon(self, trainer_id: int, pokemon_id: int) -> dict:
        return self.db.add_new_pokemon_to_trainer(trainer_id, pokemon_id)
    
    def is_have_pokemon(self, trainer_id: int, pokemon_id: int) -> bool:
        return self.db.is_trainer_has_pokemon(trainer_id, pokemon_id)
    
class Actions_Repo:
    def __init__(self, db: DB_Interface):
        self.db = db

    def evolve_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> dict:
        return self.db.evolve_pokemon_of_trainer(trainer_id, old_pokemon_id, new_pokemon_id)