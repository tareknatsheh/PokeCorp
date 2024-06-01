from typing import Optional
from fastapi import APIRouter, HTTPException, status
from Model.db import db
from Model.Entities import Pokemon

router = APIRouter()

@router.put("/{pokemon_id}/{trainer_id}", status_code=status.HTTP_200_OK)
def get_pokemon(pokemon_id: int, trainer_id: int):
    """Evolve (pokemon x of trainer y)
    Path:
        pokemon_id: int
        trainer_id: int

    Returns:
        json: updated pokemon details
    """
    pass