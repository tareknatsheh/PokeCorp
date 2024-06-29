from typing import Optional
from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status
from routes.utils.routes_error_handler import handle_route_errors
from Model.db import create_database
import requests
from decouple import config
import base64

router = APIRouter()
db = create_database()

@router.get("/", status_code=status.HTTP_200_OK)
@handle_route_errors
def get_pokemon(type: Optional[str] = None, trainer_id: Optional[int] = None):
    """Get all pokemons, or filter by parameters
    Params:
        type: string
        trainer: string

    Returns:
        json: pokemon details
    """
    result = db.pokemon.get_by_type_and_trainer_id(type, trainer_id)

    if not result:
        raise HTTPException(status_code=404, detail=f"Couldn't find any pokemon")
    
    return result

@router.post("/", status_code=status.HTTP_201_CREATED)
@handle_route_errors
def add_new_pokemon(pokemon_id: int):
    """Add a pokemon by their id

    Args:
        pokemon_id (int): The unique id defined in https://pokeapi.co/

    Returns:
        response: status of the addition
    """
    return db.pokemon.add(pokemon_id)


@router.post("/images")
async def upload_image(pokemon_id: int, file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.")
    
    result = await db.pokemon.update_image(pokemon_id, file)
    return result
    
@router.get("/images/{pokemon_id}")
@handle_route_errors
def get_pokemon_image_by_id(pokemon_id: int):
    url = str(config("IMAGES_MICROSERVICE_URI"))
    response = requests.get(f"{url}/{pokemon_id}")

    return Response(response.content, media_type="image/jpeg")
