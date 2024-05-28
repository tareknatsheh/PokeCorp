from typing import Optional
from fastapi import APIRouter, Path, HTTPException
from Model.db import db
from Model.Entities import Pokemon

router = APIRouter()

@router.get("/")
def get_pokemon(type: Optional[str] = None, trainer: Optional[str] = None):
    """Get all pokemons, or filter by parameters
    Params:
        type: string
        trainer: string

    Returns:
        json: pokemon details
    """

    pokemon = db.find_by_type_and_trainer(type, trainer)

    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Couldn't find any pokemon")
    
    return pokemon



@router.get("/{id}")
def get_pokemon_by_id(id: int = Path(title="id of pokemon to get from DB")):
    """Get pokemon by their unique id

    Returns:
        json: pokemon details
    """
    pokemon = db.find_pokemon_by_id(id)
    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokemon with id {id} could not be found")
    
    return pokemon

""" ??
DELETE /{trainer_id}/pokemon/{pokemon_id}
5. delete pokemon of trainer
"""

"""
POST /
payload:
{ id, name, height, weight, types (all of them) }
1. Add new pokemon species: adds a new pokemon species

"""
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