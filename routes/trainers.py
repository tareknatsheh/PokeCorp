from typing import Optional
from fastapi import APIRouter, Path, HTTPException, status
from Model.db import create_database
from routes.utils.routes_error_handler import handle_route_errors
from Model.Entities import Pokemon, Trainer

router = APIRouter()
db = create_database()

@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_trainers_by_pokemon_id(pokemon_id: Optional[int] = None):
    """Get all trainers, or filter by pokemon they have
    Params:
        pokemon_id: int

    Returns:
        json: trainers
    """
    result: list[Trainer] = []
    if pokemon_id:
        result = db.trainer.get_by_pokemon_id(pokemon_id)
    else:
        result = db.trainer.get_all()

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any trainer")

    return result

# @router.put("/{trainer_id}/pokemon/{pokemon_id}")
# @handle_route_errors
# def delete_trainer_pokemon_relation(trainer_id: int, pokemon_id: int):
#     """Take a pokemon away from a trainer
#     Path:
#         trainer_id: int
#         pokemon_id: int
#     Returns:
#         json: the deletion status
#     """
#     try:
#         result = db.remove_relation_between(trainer_id, pokemon_id)
#         return {
#             "number of affected rows": result
#         }

#     except Exception as e:
#         print(f"{e}")
#         raise HTTPException(status_code=500, detail=f"Something went wrong, check the logs")


@router.put("/{trainer_id}/pokemons")
@handle_route_errors
def add_new_pokemon(trainer_id: int, pokemon_id: int) -> Pokemon:
    """add pokemon to a trainer: when a trainer catches a pokemon and train it the pokemon become his.
    params:
        pokemon_id
    """

    if not pokemon_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A Pokemon ID must be provided")
    
    return db.trainer.add_new_pokemon(trainer_id, pokemon_id)


