import base64
from fastapi import HTTPException, UploadFile
import requests

async def update_image_of_pokemon_by_id(file: UploadFile, url: str, pokemon_id: int):
    if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and GIF are allowed.")
    
    image_data = await file.read()
    encoded_string = base64.b64encode(image_data)

    # send data to mongodb-imgs-microservice
    print(f"passing data to {url}")

    payload ={"pokemon_id": pokemon_id, "filedata": encoded_string, "content_type": file.content_type}
    response = requests.post(url, data=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=response.json()["detail"]) from http_err

    return {
        "filename": file.filename,
        "status": response.status_code,
        "details": str(response.content)
        }

def get_pok_img_by_id(url: str, pokemon_id: int) -> requests.Response:
    response = requests.get(f"{url}/{pokemon_id}")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=response.json()["detail"]) from http_err
    return response