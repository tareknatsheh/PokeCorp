from Model.Entities import Pokemon

def test_can_create_pokemon_instance():
    pok = Pokemon(id=2, name="pikatcho", height=10.5, weight=5.6, type=["grass"])
    assert pok.id == 2
    assert pok.name == "pikatcho"
    assert pok.height == 10.5
    assert pok.weight == 5.6
    assert pok.type == ["grass"]

