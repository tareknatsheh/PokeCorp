if __name__ == "__main__":
    import json
    import requests
    
    FILE_PATH = "./Model/pokemons_data.json"
    
    with open(FILE_PATH, "r+") as f:
        f.seek(0)
        all_poks = json.load(f)

        for pokemon in all_poks:
            poke_name = pokemon["name"]
            r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_name}")
            poke_real_types = r.json()["types"]
            poke_real_types_clean = [t["type"]["name"] for t in poke_real_types]

            pokemon["type"] = poke_real_types_clean
        
        f.seek(0)  
        print("updating .json file")
        json.dump(all_poks,f, indent=4)
        f.truncate()


    # for pokemon in res:
    #     poke_name = pokemon["name"]
    #     r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_name}")
    #     poke_real_types = r.json()["types"]
    #     poke_real_types_clean = [t["type"]["name"] for t in poke_real_types]


    #     if type(pokemon["type"]) == str:
    #         if not pokemon["type"] in poke_real_types_clean:
    #             print(f"{poke_name} has {pokemon["type"]} which is not in {poke_real_types_clean}")
    #     elif type(pokemon["type"]) == list:
    #         poke_internal_type = pokemon["type"]
    #         if not set(poke_internal_type).issubset(set(poke_real_types_clean)):
    #             print(f"{poke_name} has {poke_internal_type} but it should be {poke_real_types_clean}")

