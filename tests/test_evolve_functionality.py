from pytest import fixture
from routes.utils.evolve_helper import _find_next_evolution_name_and_id
import tests.utils.chains as chains

@fixture
def bulbasaur_chain():
    return chains.bulbasaur

@fixture
def weedle_chain():
    return chains.weedle

def test_find_next_evolution_name_and_id_for_bulbasaur(bulbasaur_chain):
    pokemon_name = "bulbasaur"
    evo_pokemon_name, evo_pokemon_id = _find_next_evolution_name_and_id(bulbasaur_chain, pokemon_name)
    assert evo_pokemon_name == "ivysaur"
    assert evo_pokemon_id == 2

def test_find_next_evolution_name_and_id_for_ivysaur(bulbasaur_chain):
    pokemon_name = "ivysaur"
    evo_pokemon_name, evo_pokemon_id = _find_next_evolution_name_and_id(bulbasaur_chain, pokemon_name)
    assert evo_pokemon_name == "venusaur"
    assert evo_pokemon_id == 3

def test_find_next_evolution_name_and_id_for_venusaur(bulbasaur_chain):
    pokemon_name = "venusaur"
    evo_pokemon_name, evo_pokemon_id = _find_next_evolution_name_and_id(bulbasaur_chain, pokemon_name)
    assert evo_pokemon_name == None
    assert evo_pokemon_id == None


def test_find_next_evolution_name_and_id_for_weedle(weedle_chain):
    pokemon_name = "weedle"
    evo_pokemon_name, evo_pokemon_id = _find_next_evolution_name_and_id(weedle_chain, pokemon_name)
    assert evo_pokemon_name == "kakuna"
    assert evo_pokemon_id == 14

def test_find_next_evolution_name_and_id_for_kakuna(weedle_chain):
    pokemon_name = "kakuna"
    evo_pokemon_name, evo_pokemon_id = _find_next_evolution_name_and_id(weedle_chain, pokemon_name)
    assert evo_pokemon_name == "beedrill"
    assert evo_pokemon_id == 15

def test_find_next_evolution_name_and_id_for_beedrill(weedle_chain):
    pokemon_name = "beedrill"
    evo_pokemon_name, evo_pokemon_id = _find_next_evolution_name_and_id(weedle_chain, pokemon_name)
    assert evo_pokemon_name == None
    assert evo_pokemon_id == None

