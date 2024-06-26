import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from routes.utils.routes_error_handler import handle_route_errors
from config import frontend_folder_name

router = APIRouter()

# a nice landing page for PokeCorp
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
@handle_route_errors
def read_root():
    html_file_path = os.path.join(frontend_folder_name, "index.html")
    with open(html_file_path, 'r') as html_file:
        return html_file.read()

    
