from fastapi import APIRouter, Path, HTTPException
from Model.db import db

router = APIRouter()

@router.get("/pokemon/{id}")
def get_students(id: int = Path(title="id of pokemon to get from DB")):
    """Get pokemon by their unique id

    Returns:
        json: pokemon details
    """
    pokemon = db.findById(id)
    if not pokemon:
        raise HTTPException(status_code=404, detail=f"Pokemon with id {id} could not be found")
    
    return pokemon