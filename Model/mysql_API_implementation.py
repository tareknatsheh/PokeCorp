import sys
from fastapi import HTTPException, status
sys.path.append('D:/backend-bootcamp/Final project/PokeCorp')  # Adjust the path as necessary


from decouple import config, UndefinedValueError
from Model.Entities import Pokemon, Trainer
from Model.DB_Interface import DB_Interface
import requests as req

class MySql_API_repo(DB_Interface):
    def __init__(self):
        try:
            self.db_uri: str = str(config("MYSQL_MICROSERVICE_URI"))
            self.pokemons_enpoint = f"{self.db_uri}/pokemons"
            self.trainers_enpoint = f"{self.db_uri}/trainers"
            self.evolve_enpoint = f"{self.db_uri}/evolve"
        except UndefinedValueError as e:
            print("Please set an env variable called MYSQL_MICROSERVICE_URI for the MySQL API endpoint")
            raise e
        

    def get_pokemons_by_type(self, type: str) -> list[dict]:
        res = req.get(f"{self.pokemons_enpoint}", params={"type": type})
        try:
            res.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=res.status_code, detail=res.json()["detail"]) from http_err
        return res.json()
    
    def get_pokemons_by_trainer_id(self, id: int) -> list[dict]:
        res = req.get(f"{self.pokemons_enpoint}", params={"trainer_id": id})
        try:
            res.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=res.status_code, detail=res.json()["detail"]) from http_err
        return res.json()


    def add_new_pokemon(self, pokemon_id: int) -> dict:
        # check if we already have this pokemon in our database
        res_pokemon = req.get(f"{self.pokemons_enpoint}/{pokemon_id}")

        if not res_pokemon.status_code == 404:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Pokemon with id {pokemon_id} already exists")

        # get pokemon details from https://pokeapi.co/
        poke_details = req.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        print(poke_details)
        try:
            poke_details.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            message = f"Pokemon with id {pokemon_id} does not exist" if poke_details.status_code == 404 else "something went wrong with the pokeapi.co/ API"
            raise HTTPException(status_code=poke_details.status_code, detail=message) from http_err

        poke_details = poke_details.json()
        pokemon_types_list = [t["type"]["name"] for t in poke_details["types"]]

        new_pokemon_obj = {
            "id": pokemon_id,
            "name": poke_details["name"],
            "height": poke_details["height"],
            "weight": poke_details["weight"],
            "type": pokemon_types_list
        }
        
        res = req.post(f"{self.pokemons_enpoint}", json=new_pokemon_obj)
        try:
            res.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=res.status_code, detail=res.json()["detail"]) from http_err
        print(res)
        return new_pokemon_obj
    
    def get_trainers_by_pokemon_id(self, pokemon_id: int) -> list[Trainer]:
        res = req.get(f"{self.trainers_enpoint}", params={"pokemon_id": pokemon_id})
        try:
            res.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=res.status_code, detail=res.json()["detail"]) from http_err
        return res.json()

    def add_new_pokemon_to_trainer(self, trainer_id: int, pokemon_id: int) -> dict:
        res = req.put(f"{self.trainers_enpoint}/{trainer_id}/{pokemon_id}")
        try:
            res.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=res.status_code, detail=res.json()["detail"]) from http_err
        
        return res.json()
    

    def is_trainer_has_pokemon(self, trainer_id: int, pokemon_id) -> bool:
        res  = self.get_pokemons_by_trainer_id(trainer_id)
        for pok in res:
            if pok["id"] == pokemon_id:
                return True
        
        return False
    
    def evolve_pokemon_of_trainer(self, trainer_id: int, old_pokemon_id: int, new_pokemon_id: int) -> dict:
        remove_result =  self.delete_pokemon_of_trainer(trainer_id, old_pokemon_id)
        if not "affected_rows" in remove_result:
            raise Exception("The pokemons db api did not return the expected result that has 'affected_rows' kvp")
        if remove_result["affected_rows"] <= 0:
            raise Exception("The affected_rows are 0 or less,, it should be 1")
        add_result = self.add_new_pokemon_to_trainer(trainer_id, new_pokemon_id)
        return {
            "message": f"pokemon with id {old_pokemon_id} has been removed. and pokemon with id {new_pokemon_id} has been added to trainer with id {trainer_id}",
            "new_pokemon_details": add_result["pokemon"]
        }

    def delete_pokemon_of_trainer(self, trainer_id: int, pokemon_id: int) -> dict:
        res = req.delete(f"{self.trainers_enpoint}/{trainer_id}/{pokemon_id}")
        try:
            res.raise_for_status()
        except req.exceptions.HTTPError as http_err:
            raise HTTPException(status_code=res.status_code, detail=res.json()["detail"]) from http_err
        res = res.json()
        return res

    def _before(self):
        print("connecting to db ......")
    
    def _after(self):
        print("Done - connection is closed")


if __name__ == "__main__":
    # Sanity checking the DB repo
    mysql = MySql_API_repo()
    res = mysql.get_pokemons_by_type("abbas")
    print(res)
    # a_pok = mysql.get_pokemon_by_id(34)
    # print(a_pok)
        
    