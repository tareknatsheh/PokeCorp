from fastapi import FastAPI
from routes import pokemons, trainers

app = FastAPI()

app.include_router(pokemons.router, prefix="/pokemons", tags=["Pokemons endpoint"])
app.include_router(trainers.router, prefix="/trainers",tags=["Trainers endpoint"])
