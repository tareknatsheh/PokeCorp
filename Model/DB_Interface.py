from abc import ABC, abstractmethod
from typing import Optional
from Model.Entities import Pokemon, Trainer

class DB_Interface(ABC):
    #-------- Pokemon --------
    @abstractmethod
    def add_new_pokemon(self, new_pokemon: Pokemon) -> Pokemon:
        pass

    @abstractmethod
    def get_pokemon_by_id(self, id: int) -> Pokemon:
        pass

    @abstractmethod
    def get_pokemons_by_trainer_id(self, id: int) -> list[dict]:
        pass

    @abstractmethod
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        pass

    @abstractmethod
    def get_pokemons_by_type_and_trainer_id(self, type: str, trainer_id: int) -> list[dict]:
        pass

    #-------- Trainer --------
    @abstractmethod
    def get_trainers_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        pass
    
    @abstractmethod
    def get_all_trainers(self) -> list[Trainer]:
        pass
    
    @abstractmethod
    def add_new_pokemon_to_trainer(self, trainer_id: int, new_pokemon: Pokemon) -> Pokemon:
        pass

    @abstractmethod
    def get_trainer_by_id(self, trainer_id: int) -> Optional[Trainer]:
        pass

    @abstractmethod
    def is_trainer_has_pokemon(self, trainer_id: int, pokemon_id) -> bool:
        pass