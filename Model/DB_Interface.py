from abc import ABC, abstractmethod
from typing import Optional
from Model.Entities import Pokemon, Trainer

class DB_Interface(ABC):
    #------- optional ------
    @abstractmethod
    def _before(self):
        pass
    @abstractmethod
    def _after(self):
        pass
    #-------- Pokemon --------
    @abstractmethod
    def add_new_pokemon(self, pokemon_id: int) -> dict:
        pass

    @abstractmethod
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        pass

    @abstractmethod
    def get_pokemons_by_trainer_id(self, id: int) -> list[dict]:
        pass

    #-------- Trainer --------
    @abstractmethod
    def get_all_trainers() -> list[Trainer]:
        pass
    
    @abstractmethod
    def is_trainer_has_pokemon(self, trainer_id, pokemon_id) -> bool:
        pass

    @abstractmethod
    def get_trainers_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        pass

    @abstractmethod
    def delete_pokemon_of_trainer(self, trainer_id: int, pokemon_id: int) -> dict:
        pass
    
    @abstractmethod
    def add_new_pokemon_to_trainer(self, trainer_id: int, pokemon_id: int) -> dict:
        pass

    #-------- Actions --------
    @abstractmethod
    def evolve_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> dict:
        pass
