from abc import ABC, abstractmethod
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