from abc import ABC, abstractmethod
from Model.Entities import Pokemon

class Pokemon_DB_Interface(ABC):
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