
import sys
sys.path.append('D:/backend-bootcamp/Final project/PokeCorp')  # Adjust the path as necessary


from decouple import config
from pymongo import MongoClient
from Model.Entities import Pokemon, Trainer
from typing import Optional
from Model.DB_Interface import DB_Interface
from Model.utils.db_error_handler import handle_database_errors
import Model.sql_queries.pokemon_queries as pok_queries
import Model.sql_queries.trainer_queries as tr_queries
from pymongo.collection import Collection

class MongoDB_repo(DB_Interface):
    def __init__(self):
        client: MongoClient = MongoClient(str(config("MONGO_DB_CONNECTION_STRING")))
        cursor = client[str(config("MONGO_DB_DATABASE"))]
        self.collection: Collection = cursor[str(config("MONGO_DB_COLLECTION"))]

    # @handle_database_errors
    # def get_all_pokemons(self):
    #     return self.collection.find({})
    
    @handle_database_errors
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        result = list(self.collection.find({"type": type}))
        return result
    
    @handle_database_errors
    def get_pokemons_by_trainer_id(self, trainer_id: int) -> list[dict]:
        result = list(self.collection.find({"ownedBy.id": trainer_id}))
        return result
    
    @handle_database_errors
    def get_pokemons_by_type_and_trainer_id(self, type, trainer_id) -> list[dict]:
        result = list(self.collection.find({"type": type, "ownedBy.id": trainer_id}))
        return result

    @handle_database_errors
    def get_pokemon_by_id(self, id: int) -> Optional[Pokemon]:
        result = self.collection.find_one({"id": id})
        if not result:
            return None
        return Pokemon(id=result["id"], name=result["name"], height=result["height"], weight=result["weight"], type=result["type"])

    @handle_database_errors
    def add_new_pokemon(self, new_pok: Pokemon) -> Pokemon:
        self.collection.insert_one({
            "id": new_pok.id,
            "name": new_pok.name,
            "height": new_pok.height,
            "weight": new_pok.weight,
            "type": new_pok.type
            })
        return new_pok
    
    @handle_database_errors
    def get_trainers_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_BY_POKEMON_ID, (pokemon_id,))
        result = self.cursor.fetchall()

        if not result:
            return []
        return [Trainer(id=t[0], name=t[1], town=t[2]) for t in result]
    
    @handle_database_errors
    def get_all_trainers(self) -> list[Trainer]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_ALL)
        result = self.cursor.fetchall()

        if not result:
            return []
        return [Trainer(id=t[0], name=t[1], town=t[2]) for t in result]
    
    @handle_database_errors
    def get_trainer_by_id(self, trainer_id: int) -> Optional[Trainer]:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_BY_ID, (trainer_id,))
        result = self.cursor.fetchone()
        if not result:
            return None
        return Trainer(id=result[0], name=result[1], town=result[2])
    
    @handle_database_errors
    def is_trainer_has_pokemon(self, trainer_id: int, pokemon_id) -> bool:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(tr_queries.GET_TRAINER_POKEMON, (trainer_id, pokemon_id))
        result = self.cursor.fetchone()
        if not result:
            return False
        return True
    
    @handle_database_errors
    def add_new_pokemon_to_trainer(self, trainer_id: int, pokemon: Pokemon) -> Pokemon:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        values = (trainer_id, pokemon.id)
        self.cursor.execute(tr_queries.ADD_POKEMON, values)
        self.db_connection.commit()

        return pokemon
    

    @handle_database_errors
    def remove_relation_between(self, trainer_id, pokemon_id) -> int:
        query = """
            DELETE FROM pokemon_trainers
            WHERE trainer_id = %s AND pokemon_id = %s
        """

        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(query, (trainer_id, pokemon_id))
        rows_affected = self.cursor.rowcount
        return rows_affected
    
    @handle_database_errors
    def update_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> None:
        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        values = (new_pokemon_id, trainer_id, old_pokemon_id)
        self.cursor.execute(tr_queries.EVOLVE_POKEMON, values)
        self.db_connection.commit()


    def _before(self):
        print("connecting to db ......")

    
    def _after(self):
        print("done")


if __name__ == "__main__":
    # Sanity checking the DB repo
    mysql = MongoDB_repo()
    a_pok = mysql.get_pokemon_by_id(3)
    print(a_pok)
        
    