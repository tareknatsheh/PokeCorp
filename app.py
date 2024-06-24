import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes import pokemons, trainers, evolve, home

app = FastAPI()

app.mount("/static", StaticFiles(directory=os.path.join("public", "static")), name="static")

# Add CORS Middleware
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router, prefix="", tags=["Home"])
app.include_router(pokemons.router, prefix="/pokemons", tags=["Pokemons endpoint"])
app.include_router(trainers.router, prefix="/trainers",tags=["Trainers endpoint"])
app.include_router(evolve.router, prefix="/evolve",tags=["Evolution endpoint"])