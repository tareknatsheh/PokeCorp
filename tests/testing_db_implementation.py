from typing import Optional
from Model.DB_Interface import DB_Interface
from Model.Entities import Pokemon, Trainer


class Testing_repo(DB_Interface):
    def __init__(self):
        print("Initializing the testing repo")
        self.pokemons_db = []
        self.trainers_db = []

    def _before(self):
        pass
        
    
    def _after(self):
        pass
    
    def add_new_pokemon(self, new_pokemon: Pokemon) -> Pokemon:
        pokemon_dict = new_pokemon.model_dump()
        print(f"Adding: {pokemon_dict}")
        self.pokemons_db.append(new_pokemon)
        return new_pokemon

    
    def get_pokemon_by_id(self, id: int) -> Pokemon:
        return Pokemon(id=0, name="test", height=0, weight=0, type=[])

    
    def get_pokemons_by_trainer_id(self, id: int) -> list[dict]:
        return []

    
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        return []

    
    def get_pokemons_by_type_and_trainer_id(self, type: str, trainer_id: int) -> list[dict]:
        return []

    #-------- Trainer --------
    
    def get_trainers_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        return []
    
    
    def get_all_trainers(self) -> list[Trainer]:
        return []
    
    
    def add_new_pokemon_to_trainer(self, trainer_id: int, new_pokemon: Pokemon) -> Pokemon:
        return Pokemon(id=0, name="test", height=0, weight=0, type=[])

    
    def get_trainer_by_id(self, trainer_id: int) -> Optional[Trainer]:
        pass

    
    def is_trainer_has_pokemon(self, trainer_id: int, pokemon_id) -> bool:
        return False
    
    def evolve_pokemon_of_trainer(self, pokemon_id: int, trainer_id: int) -> Pokemon:
        return Pokemon(id=0, name="test", height=0, weight=0, type=[])