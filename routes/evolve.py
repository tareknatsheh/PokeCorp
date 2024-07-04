from fastapi import APIRouter, HTTPException, status
from Model.db import create_database
from routes.utils.evolve_helper import evolve
from routes.utils.routes_error_handler import handle_route_errors

router = APIRouter()
db = create_database()

@router.put("/{pokemon_id}/{trainer_id}", status_code=status.HTTP_200_OK)
@handle_route_errors
def evolve_pokemon(pokemon_id: int, trainer_id: int):
    """Evolve (pokemon x of trainer y)
    Path:
        pokemon_id: int
        trainer_id: int

    Returns:
        json: updated pokemon details
    """

    # First, check if this trainer indeed has this pokemon:
    does_trainer_has_pokemon: bool = db.trainer.is_have_pokemon(trainer_id, pokemon_id)
    if not does_trainer_has_pokemon:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"This trainer with id {trainer_id} does not own this pokemon with id {pokemon_id}")
    
    next_pok_name, next_pok_id = evolve(pokemon_id)
    print(f"Next pok: {next_pok_name}, id: {next_pok_id}")
    print(f"type of the id is: {type(next_pok_id)}")


    if not next_pok_id or not next_pok_name:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Pokemon with id {pokemon_id} can not evolve further.")
    
    # Second, let's check if trainer already has the evolved version
    does_trainer_has_new_pokemon: bool = db.trainer.is_have_pokemon(trainer_id, next_pok_id)

    if does_trainer_has_new_pokemon:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"Trainer with id {trainer_id} already has the evolved version of {pokemon_id}")
    
    # update the database
    ev_result = db.actions.evolve_pokemon_of_trainer(trainer_id, pokemon_id, next_pok_id)

    # TODO
    # make sure that we have the image of the new pokemon in our images database
    # url = str(config("IMAGES_MICROSERVICE_URI"))
    # response = requests.get(f"{url}/{pokemon_id}")

    return ev_result
