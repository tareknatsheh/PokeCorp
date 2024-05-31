GET_BY_POKEMON_ID = """
    SELECT tr.id, tr.name, tr.town
    FROM (SELECT * FROM pokemons WHERE id = %s) p
    LEFT JOIN pokemon_trainers pktr ON p.id = pktr.pokemon_id
    LEFT JOIN trainers tr ON pktr.trainer_id = tr.id
"""