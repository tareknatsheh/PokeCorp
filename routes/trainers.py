from typing import Optional
from fastapi import APIRouter, Path, HTTPException
from Model.db import db
from routes.utils.routes_error_handler import handle_route_errors
from Model.Entities import Trainer

router = APIRouter()

# TODO improve returned result and make sure status code is clear

@router.get("/")
@handle_route_errors
def get_trainers_by_pokemon_id(pokemon_id: Optional[int] = None):
    """Get all trainers, or filter by pokemon they have
    Params:
        pokemon_id: int

    Returns:
        json: trainers
    """
    result = None
    if pokemon_id:
        result: list[Trainer] | None = db.trainer.get_by_pokemon_id(pokemon_id)
    else:
        # result = db.find_all_trainers()
        print("")

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any trainer")

    return result


# @router.get("/{id}")
# @handle_route_errors
# def get_trainer(id: int = Path(title="id of pokemon to get from DB")):
#     """Get trainer by id
#     Path:
#         id: int
#     Returns:
#         json: trainer
#     """

#     result = None
#     if not id:
#         raise HTTPException(status_code=400, detail=f"Trainer id is null")

#     result = db.find_trainer_by_id(id)

#     if not result:
#         raise HTTPException(status_code=404, detail=f"Couldn't find any trainer with id {id}")

#     return result

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


# @router.post("/{trainer_id}/pokemons")
# @handle_route_errors
# def add_new_pokemon(trainer_id: int, pokemon_id: int):
#     """add pokemon to a trainer: when a trainer catches a pokemon and train it the pokemon become his
#     params:
#         pokemon_id
#     """

#     return "test"

