GET_BY_TYPE = """
    SELECT pk.id, pk.name, pk.height, pk.weight 
    FROM (SELECT * FROM types WHERE type = %s) ty
    LEFT JOIN pokemons pk ON ty.pokemon_id = pk.id;
""" 
GET_BY_TRAINER_ID = """
    SELECT p.id, p.name, p.height, p.weight
    FROM (SELECT * FROM pokemon_trainers WHERE trainer_id = %s) pktr
    LEFT JOIN pokemons p ON p.id = pktr.pokemon_id;
"""
GET_BY_TYPE_AND_TRAINER_ID = """
    SELECT p.id, p.name, p.height, p.weight
    FROM (SELECT * FROM pokemon_trainers WHERE trainer_id = %s) pktr
    INNER JOIN pokemons p ON p.id = pktr.pokemon_id
    INNER JOIN (SELECT * FROM types WHERE type = %s) ty ON p.id = ty.pokemon_id;
"""
GET_BY_ID = "SELECT id, name, height, weight FROM pokemons WHERE id = %s"
GET_TYPES = "SELECT pokemon_id, type FROM types WHERE pokemon_id = %s"
ADD = "INSERT INTO pokemons (id, name, height, weight) VALUES (%s, %s, %s, %s)"
ADD_TYPES = "INSERT INTO types (pokemon_id, type) VALUES (%s, %s)"
