from fastapi import APIRouter, HTTPException, status
from Model.db import create_database
from Model.Entities import Pokemon
from routes.utils.evolve_helper import Evolve
from routes.utils.routes_error_handler import handle_route_errors

router = APIRouter()
db = create_database()

@router.put("/{pokemon_id}/{trainer_id}", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_pokemon(pokemon_id: int, trainer_id: int):
    """Evolve (pokemon x of trainer y)
    Path:
        pokemon_id: int
        trainer_id: int

    Returns:
        json: updated pokemon details
    """
    evolve = Evolve()
    evolve.evolve(pokemon_id)
    next_pok_name = evolve.get_evolve_name()
    next_pok_id = evolve.get_evolve_id()

    return {
        "name": next_pok_name,
        "id": next_pok_id
    }
