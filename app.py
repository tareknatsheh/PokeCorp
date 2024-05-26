from fastapi import FastAPI
from Model.db import db

app = FastAPI

@app.get("/")
def find_pokemon_by_type(poke_type: str):
    # pokemon_names = find_pokemon_by_type(poke_type)
    pokemon_names = db.findByType(poke_type)
    return {"pokemon_names": pokemon_names}


@app.get("/{pokemon_name}")
def find_trainers_by_pokemon(pokemon_name: str):
    trainer_names = db.findByOwner(pokemon_name)
    return {"trainer_names": trainer_names}


@app.get("/{trainer_name}")
def find_pokemons_by_trainer(trainer_name: str):
  
  pokemon_names = db.PokemonsOfTrainer(trainer_name)
  return {"pokemon_names": pokemon_names}

