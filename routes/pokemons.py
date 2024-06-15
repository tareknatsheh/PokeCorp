from typing import Optional
from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status
from routes.utils.routes_error_handler import handle_route_errors
from Model.db import create_database
from Model.Entities import Pokemon
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
    result = None
    if not type:
        if not trainer_id:
            raise HTTPException(status_code=400, detail=f"There are too many pokemons, please specify a type and/or a trainer")
        else:
            result = db.pokemon.get_by_trainer_id(trainer_id)
    else:
        result = db.pokemon.get_by_type(type)

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
    try:
        if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.")
        
        image_data = await file.read()
        encoded_string = base64.b64encode(image_data)
        # send data to mongodb-imgs-microservice
        url = str(config("IMAGES_MICROSERVICE_URI"))
        print(f"passing data to {url}")

        payload ={"pokemon_id": pokemon_id, "filedata": encoded_string, "content_type": file.content_type}
        response = requests.post(url, data=payload)

        return {
            "filename": file.filename,
            "status": response.status_code,
            "details": str(response.content)
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/images/{pokemon_id}")
def get_pokemon_image_by_id(pokemon_id: int):
    url = str(config("IMAGES_MICROSERVICE_URI"))
    response = requests.get(f"{url}/{pokemon_id}")

    return Response(response.content, media_type="image/jpeg")
