from Model.Entities import Pokemon
from Model.mysql_repo import MySql_repo as repo
from typing import Optional

class Database:
    def __init__(self):
        self.my_db = repo()
        pass
    
    # done
    def find_by_type_and_trainer(self, type: Optional[str], trainer_name: Optional[str]) -> list[dict]:
        return self.my_db.find_and_filter_type_trainer(type, trainer_name)

    # done
    def find_pokemon_by_id(self, id: int) -> Pokemon | None:
        try:
            return self.my_db.get_pokemon_by_id(id)
        except Exception as e:
            print(f"Error: find_by_id: {e}")
            raise
    
    # done
    def find_all_pokemons(self) -> list[dict]:
        return self.my_db.find_and_filter_type_trainer(None, None)

    # done
    def find_pokemon_by_type(self, type: str) -> list[dict]:
        return self.my_db.find_and_filter_type_trainer(type, None)
    
    # TODO
    def find_trainers(self, pokemon_name: str) -> list[str]:
        return []
    
    # done
    def find_pokemons_by_trainer(self, trainer_name) -> list[dict]:
        return self.my_db.find_and_filter_type_trainer(None, trainer_name)
    
    # done
    def add_new_pokemon(self, new_pok: Pokemon):
        try:
            return self.my_db.add_new_pokemon(new_pok)
        except Exception as e:
            print(f"Error: add_new_pokemon: {e}")
            raise


db = Database()