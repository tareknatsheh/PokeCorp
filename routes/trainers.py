from fastapi import APIRouter, HTTPException, status
from Model.db import create_database
from routes.utils.routes_error_handler import handle_route_errors
from Model.Entities import Trainer

router = APIRouter()
db = create_database()

@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_trainers_by_pokemon_id(pokemon_id: int | None = None):
    """Get trainers by pokemon they have
    Params:
        pokemon_id: int

    Returns:
        json: trainers
    """
    result: list[Trainer] = []
    if not pokemon_id:
        result = db.trainer.get_all()
    else:
        result = db.trainer.get_by_pokemon_id(pokemon_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any trainer")

    return result

@router.delete("/{trainer_id}/{pokemon_id}")
@handle_route_errors
def delete_pokemon_of_trainer(trainer_id: int, pokemon_id: int):
    """Take a pokemon away from a trainer
    Path:
        trainer_id: int
        pokemon_id: int
    Returns:
        json: the deletion status
    """

    result = db.trainer.delete_a_pokemon(trainer_id, pokemon_id)
    return {
        "affected_trainers": result
    }



@router.put("/{trainer_id}/{pokemon_id}")
@handle_route_errors
def add_new_pokemon_to_trainer(trainer_id: int, pokemon_id: int):
    """add pokemon to a trainer: when a trainer catches a pokemon and trains it the pokemon become his.
        path:
            pokemon_id
    """

    if not pokemon_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A Pokemon ID must be provided")
    
    res = db.trainer.add_new_pokemon(trainer_id, pokemon_id)
    return res


