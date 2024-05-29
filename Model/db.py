from Model.Pokemon_DB_Interface import Pokemon_DB_Interface
from Model.Repositories import Pokemon_Repo
from Model.mysql_implementation import MySql_repo
import Model.sql_queries.pokemon_queries as pk_quries
import Model.sql_queries.trainer_queries as tr_queries


# TODO refactor to something like this: db.trainer.add(...)

class Database:
    def __init__(self):
        self.my_db: Pokemon_DB_Interface = MySql_repo()
        self.pokemon = Pokemon_Repo(self.my_db)
        pass
    
    # -------- Pokemon -----------
    # # done
    # def find_pokemon_by_id(self, id: int) -> Pokemon | None:
    #     try:
    #         return self.my_db.get_pokemon_by_id(id)
    #     except Exception as e:
    #         print(f"Error: find_by_id: {e}")
    #         raise
    
    # # done
    # def find_pokemon_by_type(self, type: str) -> list[dict]:
    #     return self.my_db.find_pokemon_by_type(type)
    
    # # done
    # def find_pokemons_by_trainer_id(self, trainer_name) -> list[dict]:
    #     return self.my_db.find_pokemons_by_trainer_id(trainer_name)
    
    # def find_pokemons_by_type_and_trainer_id(self, type, trainer_name):
    #     return self.my_db.find_pokemons_by_type_and_trainer_id(type, trainer_name)
    
    # # done
    # def add_new_pokemon(self, new_pok: Pokemon):
    #     try:
    #         return self.my_db.add_new_pokemon(new_pok)
    #     except Exception as e:
    #         print(f"Error: add_new_pokemon: {e}")
    #         raise
    
    # # -------- Trainer -----------
    # def find_trainers_by_pokemon_id(self, pokemon_id: int):
    #     return self.my_db.find_trainers_by_pokemon_id(pokemon_id)
    
    # def find_all_trainers(self):
    #     return self.my_db.find_all_trainers()
    
    # def find_trainer_by_id(self, trainer_id):
    #     return self.my_db.find_trainer_by_id(trainer_id)
    
    # def remove_relation_between(self, trainer_id, pokemon_id) -> int:
    #     return self.my_db.remove_relation_between(trainer_id, pokemon_id)




db = Database()