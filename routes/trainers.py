from typing import Optional
from fastapi import APIRouter, Path, HTTPException
from Model.db import db

router = APIRouter()

@router.get("/")
def get_trainer_by_pokemon_id(pokemon_id: Optional[int] = None):
    """Get all trainers, or filter by pokemon they have
    Params:
        pokemon_id: int

    Returns:
        json: trainers
    """
    result = None
    if pokemon_id:
        result = db.find_trainers_by_pokemon_id(pokemon_id)
    else:
        result = db.find_all_trainers()

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any trainer")

    return result


@router.get("/{id}")
def get_trainer(id: int = Path(title="id of pokemon to get from DB")):
    pass

""" ??
PUT, PATCH ?
DELETE /{trainer_id}/pokemon/{pokemon_id}
5. delete pokemon of trainer
"""

"""
POST /{trainer_id}/pokemons
payload:
{ Pokemon name or id }
6. add pokemon to a trainer: when a trainer catches a pokemon and train it the pokemon become his.
"""

