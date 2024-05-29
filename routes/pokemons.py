from typing import Optional
from fastapi import APIRouter, HTTPException
from Model.db import db
from Model.Entities import Pokemon

router = APIRouter()

# TODO improve returned result and make sure status code is clear

@router.get("/")
def get_pokemon(type: Optional[str] = None, trainer_id: Optional[str] = None):
    """Get all pokemons, or filter by parameters
    Params:
        type: string
        trainer: string

    Returns:
        json: pokemon details
    """
    result = None
    if not type:
        if not trainer_id:
            # get all pokemons
            raise HTTPException(status_code=400, detail=f"There are too many pokemons, please specify a type and/or a trainer")
        else:
            # get by trainer
            result = db.find_pokemons_by_trainer_id(trainer_id)
    else:
        if not trainer_id:
            # get by type
            result = db.find_pokemon_by_type(type)
        else:
            # get by type and trainer id
            result = db.find_pokemons_by_type_and_trainer_id(type, trainer_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any pokemon")

    return result

@router.get("/{id}")
def get_pokemon_by_id(id: int):
    """Get pokemon by their unique id

    Returns:
        json: pokemon details
    """
    pokemon = db.find_pokemon_by_id(id)
    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokemon with id {id} could not be found")
    
    return pokemon


@router.post("/")
def add_new_pokemon(new_pokemon: Pokemon) -> Pokemon:
    """
    Pyload:
        id, name, height, weight, types (all of them)
    """
    return db.add_new_pokemon(new_pokemon)



"""
PUT /evolve/{pokemon_id}/{trainer_id}
7. Evolve (pokemon x of trainer y)
"""