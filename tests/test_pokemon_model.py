import pytest
from Model.Entities import Pokemon
from tests.db_testing import create_database

@pytest.fixture
def db():
    # a new database instance for each test
    return create_database()


def test_can_create_pokemon_instance():
    pok = Pokemon(id=2, name="pikatcho", height=10.5, weight=5.6, type=["grass"])
    assert pok.id == 2
    assert pok.name == "pikatcho"
    assert pok.height == 10.5
    assert pok.weight == 5.6
    assert pok.type == ["grass"]


def test_adding_new_pokemon(db):
    new_pok = Pokemon(id=2, name="racho", height=150, weight=20, type=["fire"])
    db.pokemon.add(new_pok)
    assert new_pok in db.pokemon.get_all()

def test_getting_all_with_empty_db(db):
    assert db.pokemon.get_all() == []

def test_getting_all_with_one_pokemon(db):
    new_pok = Pokemon(id=2, name="racho", height=150, weight=20, type=["fire"])
    db.pokemon.add(new_pok)
    assert len(db.pokemon.get_all()) == 1
