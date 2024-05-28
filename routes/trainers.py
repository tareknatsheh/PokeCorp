from fastapi import APIRouter, Path, HTTPException
from Model.db import db

router = APIRouter()

"""
GET / 
Get all trainers, or filter by pokemon they have
params:
    pokemon they have
"""



@router.get("/{id}")
def get_trainer(id: int = Path(title="id of pokemon to get from DB")):
    pass



"""
POST /{trainer_id}/pokemons
payload:
{ Pokemon name or id }
6. add pokemon to a trainer: when a trainer catches a pokemon and train it the pokemon become his.
"""

