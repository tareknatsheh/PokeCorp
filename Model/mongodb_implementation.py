
# import sys
# sys.path.append('D:/backend-bootcamp/Final project/PokeCorp')  # Adjust the path as necessary


from decouple import config
from pymongo import MongoClient, ReturnDocument
from Model.Entities import Pokemon, Trainer
from typing import Optional
from Model.DB_Interface import DB_Interface
from Model.utils.db_error_handler import handle_database_errors
from pymongo.collection import Collection

class MongoDB_repo(DB_Interface):
    def __init__(self):
        client: MongoClient = MongoClient(str(config("MONGO_DB_CONNECTION_STRING")))
        cursor = client[str(config("MONGO_DB_DATABASE"))]
        self.collection: Collection = cursor[str(config("MONGO_DB_COLLECTION"))]
    
    @handle_database_errors
    def get_pokemons_by_type(self, type: str) -> list[dict]:
        result = list(self.collection.find({"type": type}, {"_id": 0}))
        return result
    
    @handle_database_errors
    def get_pokemons_by_trainer_id(self, trainer_id: int) -> list[dict]:
        result = list(self.collection.find({"ownedBy.id": trainer_id}, {"_id": 0}))
        return result
    
    @handle_database_errors
    def get_pokemons_by_type_and_trainer_id(self, type, trainer_id) -> list[dict]:
        result = list(self.collection.find({"type": type, "ownedBy.id": trainer_id}, {"_id": 0}))
        return result

    @handle_database_errors
    def get_pokemon_by_id(self, id: int) -> Optional[Pokemon]:
        result = self.collection.find_one({"id": id}, {"_id": 0})
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
        result = self.collection.find_one({"id": pokemon_id})
        if result:
            trainers_list = result["ownedBy"]
            return [Trainer(id=t["id"], name=t["name"], town=t["town"]) for t in trainers_list]
        return []
    
    @handle_database_errors
    def get_all_trainers(self) -> list[Trainer]:
        # Define the aggregation pipeline
        pipeline = [
            {"$unwind": "$ownedBy"},  # Unwind the ownedBy array to normalize the data
            {"$project": {            # Project the desired fields
                "_id": 0,             # Exclude the _id field from the output
                "id": "$ownedBy.id",
                "name": "$ownedBy.name",
                "town": "$ownedBy.town"
            }},
            {"$group": {              # Group to ensure uniqueness
                "_id": {
                    "id": "$id",
                    "name": "$name",
                    "town": "$town"
                }
            }},
            {"$project": {            # Project the final desired output structure
                "_id": 0,
                "id": "$_id.id",
                "name": "$_id.name",
                "town": "$_id.town"
            }}
        ]
        # Execute the aggregation query
        results = self.collection.aggregate(pipeline)

        if not results:
            return []
        
        return [Trainer(id=t["id"], name=t["name"], town=t["town"]) for t in results]
    
    @handle_database_errors
    def get_trainer_by_id(self, trainer_id: int) -> Optional[Trainer]:
        # Define the aggregation pipeline
        pipeline = [
            {"$unwind": "$ownedBy"},  # Unwind the ownedBy array
            {"$match": {"ownedBy.id": trainer_id}},  # Match to find the specific trainer by id
            {"$replaceRoot": {"newRoot": "$ownedBy"}},  # Replace the root of the document with the trainer subdocument
            {"$limit": 1}  # Limit the output to the first found document
        ]

        # Execute the aggregation query
        result = self.collection.aggregate(pipeline)
        # .aggregare always returns a cursor, which is an iterable object
        # we can use 'next' to get the result
        result = next(result, None) 

        if not result:
            return None
        
        return Trainer(id=result["id"], name=result["name"], town=result["town"])
    
    @handle_database_errors
    def is_trainer_has_pokemon(self, trainer_id: int, pokemon_id) -> bool:
        pok = self.collection.find_one({"id": pokemon_id})
        if not pok:
            raise ValueError(f"Could not find pokemon with id {pokemon_id}")
        
        trainers_of_this_pok = pok["ownedBy"]
        for tr in trainers_of_this_pok:
            if tr["id"] == trainer_id:
                return True

        return False
    
    @handle_database_errors
    def add_new_pokemon_to_trainer(self, trainer_id: int, pokemon: Pokemon) -> Optional[Pokemon]:
        trainer = self.get_trainer_by_id(trainer_id)
        if not trainer:
            raise ValueError(f"Could not find trainer with id {trainer_id}")
        
        # make sure that the pokemon is not already owned by this trainer:
        if self.is_trainer_has_pokemon(trainer_id, pokemon.id):
            raise ValueError(f"Trainer with id {trainer_id} already has this pokemon with id {pokemon.id}")
        
        # now lets add it
        trainer_obj = {
            "id": trainer.id,
            "name": trainer.name,
            "town": trainer.town
        }

        # Update operation to add the new trainer
        result = self.collection.update_one(
            {"id": pokemon.id},  # Filter document by Pokémon ID
            {"$push": {"ownedBy": trainer_obj}}  # Push new trainer to the 'ownedBy' array
        )

        # Check if the update was successful
        if result.modified_count > 0:
            print("Trainer added successfully.")
            return pokemon

        print("Nothing was updated!, maybe the pokemon does not exist")
        return None


    @handle_database_errors
    def remove_relation_between(self, trainer_id, pokemon_id) -> int:
        raise NotImplementedError
    
    @handle_database_errors
    def evolve_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> None:
        # verify pokemons exist before doing anything
        old_pokemon = self.collection.find_one({"id": old_pokemon_id, "ownedBy.id": trainer_id})
        new_pokemon = self.collection.find_one({"id": new_pokemon_id})
        trainer = old_pokemon and any(trainer['id'] == trainer_id for trainer in old_pokemon.get('ownedBy', []))

        if old_pokemon and new_pokemon and trainer:
            # First, find and remove the trainer from Pokémon A
            old_pokemon_object = self.collection.find_one_and_update(
                {"id": old_pokemon_id, "ownedBy.id": trainer_id},
                {"$pull": {"ownedBy": {"id": trainer_id}}},
                projection={"ownedBy.$": 1},
                return_document=ReturnDocument.BEFORE
            )

            if old_pokemon_object and 'ownedBy' in old_pokemon_object and len(old_pokemon_object['ownedBy']) > 0:
                trainer_data = old_pokemon_object['ownedBy'][0]
                # Then, add the trainer to Pokémon B
                result = self.collection.update_one(
                    {"id": new_pokemon_id},
                    {"$push": {"ownedBy": trainer_data}}
                )
                if result.modified_count > 0:
                    print(f"Trainer moved successfully from being an owner of pok with id {old_pokemon_id} to be owner of pok id {new_pokemon_id}.")
                else:
                    print(f"Failed to add trainer to pokemon with id {new_pokemon_id}.")
            else:
                print(f"Trainer not found for pokemon with id {old_pokemon_id} or failed to remove.")
        else:
            print(f"Check failed: Ensure both pokemons exist and trainer is in pokemon with id {old_pokemon_id}.")


    def _before(self):
        print("connecting to db ......")

    
    def _after(self):
        print("done")


if __name__ == "__main__":
    # Sanity checking the DB repo
    mysql = MongoDB_repo()
    a_pok = mysql.evolve_pokemon_of_trainer(4, 1, 2)
    print(a_pok)
        
    