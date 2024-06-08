import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes import pokemons, trainers, evolve, home

app = FastAPI()


app.mount("/public", StaticFiles(directory="public"), name="public")

app.include_router(home.router, prefix="", tags=["Home"])
app.include_router(pokemons.router, prefix="/pokemons", tags=["Pokemons endpoint"])
app.include_router(trainers.router, prefix="/trainers",tags=["Trainers endpoint"])
app.include_router(evolve.router, prefix="/evolve",tags=["Evolution endpoint"])