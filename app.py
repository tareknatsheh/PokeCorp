from fastapi import FastAPI
from Model.db import db
from routes import pokemon, trainer

app = FastAPI()


app.include_router(pokemon.router, tags=["Pokemons endpoint"])

# @app.get("/{pokemon_name}")
# def find_trainers_by_pokemon(pokemon_name: str):
#     trainer_names = db.findOwners(pokemon_name)
#     return {"trainer_names": trainer_names}

# @app.get("/{poke_type}")
# def find_pokemon_by_type(poke_type: str):
#     pokemon_names = db.findByType(poke_type)
#     return {"pokemon_names": pokemon_names}

# @app.get("/{trainer_name}")
# def find_pokemons_by_trainer(trainer_name: str):
#   pokemon_names = db.findPokemonsOfOwner(trainer_name)
#   return {"pokemon_names": pokemon_names}

