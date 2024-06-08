from pydantic import ValidationError
import pytest
from Model.Entities import Pokemon
from tests.db_for_testing import create_database

@pytest.fixture
def db():
    # a new database instance for each test
    return create_database()


def test_can_create_correct_pokemon_instance():
    pok = Pokemon(id=2, name="pikatcho", height=10.5, weight=5.6, type=["grass"])
    assert pok.id == 2
    assert pok.name == "pikatcho"
    assert pok.height == 10.5
    assert pok.weight == 5.6
    assert pok.type == ["grass"]

def test_cant_create_wrong_pokemon_instance():
    with pytest.raises(ValidationError):
        Pokemon(id=-2, name="pikatcho", height=10.5, weight=5.6, type=["grass"]) # invalid id
    with pytest.raises(ValidationError):
        Pokemon(id=-2, name="p"*51, height=10.5, weight=5.6, type=["grass"]) # name too long
    with pytest.raises(ValidationError):
        Pokemon(id=2, name="", height=10.5, weight=5.6, type=["grass"]) # no name
    with pytest.raises(ValidationError):
        Pokemon(id=2, name="pikatcho", height=-10.5, weight=5.6, type=["grass"]) # invalid height
    with pytest.raises(ValidationError):
        Pokemon(id=2, name="pikatcho", height=10.5, weight=-5, type=["grass"]) # invalid weight
    with pytest.raises(ValidationError):
        Pokemon(id=2, name="pikatcho", height=-10.5, weight=5.6, type="grass") # type: ignore - invalid type


def test_adding_new_pokemon(db):
    new_pok = Pokemon(id=2, name="racho", height=150, weight=20, type=["fire"])
    db.pokemon.add(new_pok)
    assert new_pok in db.my_db.pokemons_db

def test_getting_all_with_empty_db(db):
    assert db.my_db.pokemons_db == []

def test_getting_all_with_one_pokemon(db):
    new_pok = Pokemon(id=2, name="racho", height=150, weight=20, type=["fire"])
    db.pokemon.add(new_pok)
    assert len(db.my_db.pokemons_db) == 1
