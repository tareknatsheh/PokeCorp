from fastapi import HTTPException
import requests

class Evolve:
    def __init__(self):
        self.pokemon_id = None
        self.evo_pokemon_id = None
        self.evo_pokemon_name = None
        self.pokemon_name = None
        self.next = None
        self.evo_chain_url = None
        self.evo_chain_dict = None

    def _get_name_and_evolution_chain_url_by_pokemon_id(self) -> None:
        # get the pokemon details from pokeApi
        try:
            species_details = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{self.pokemon_id}")
            species_details.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.HTTPError as http_err:
            if species_details.status_code == 404:
                print("Error 404: Resource not found.")
                raise HTTPException(status_code=404, detail=f"Pokemon with id {self.pokemon_id} could not be found")
            else:
                print(f"HTTP error occurred: {http_err}")
                raise HTTPException(status_code=500, detail=f"Something went wrong with pokeAPI")
        except Exception as err:
            print(f"An error occurred: {err}")
        else:
            species_details = species_details.json()
            if not "evolution_chain" in species_details:
                raise ValueError("The species details do not have evolution chain object")
            
            if not "url" in species_details["evolution_chain"]:
                raise ValueError("The species details have evolution chain but there is no 'url' KVP inside it!")
            
            self.evo_chain_url = species_details["evolution_chain"]["url"]

            if not "name" in species_details:
                raise ValueError("The species details do not have name KVP!")
            self.pokemon_name = species_details["name"]
            print(f"Our guy is {self.pokemon_name}")

    def _get_evolution_chain_object(self):
        if not self.evo_chain_url:
            raise ValueError("You can't call _get_evolution_chain_object without having the evo chain url")
        evo_chain = requests.get(self.evo_chain_url).json()
        if not "chain" in evo_chain:
            raise ValueError("There is no 'chain' KVP in the evo chain!")
        self.evo_chain_dict = evo_chain["chain"]

    def _check_names_in_chain_recursive(self, pokemon_chain_obj):
        if not "species" in pokemon_chain_obj:
            raise ValueError("The evolution chain object is missing the 'species' KVP")
        if not "name" in pokemon_chain_obj["species"]:
            raise ValueError("The 'species' KVP inside the evolution chain object is missing the 'name' KVP")
        
        print(f"checking: {pokemon_chain_obj["species"]["name"]}")

        # check the next evolution in line:
        if not "evolves_to" in pokemon_chain_obj:
            raise ValueError("The evolution chain object is missing the 'evolves_to' KVP")
        
        if pokemon_chain_obj["evolves_to"]:
            if not pokemon_chain_obj["species"]["name"] == self.pokemon_name:
                for chain_obj in pokemon_chain_obj["evolves_to"]:
                    return self._check_names_in_chain_recursive(chain_obj)
            else:
                print(f"Found him: {pokemon_chain_obj["species"]["name"]}, let's get the next evo")
                next_evo_name = pokemon_chain_obj["evolves_to"][0]["species"]["name"]
                self.evo_pokemon_name = next_evo_name
                print(f"It will be {next_evo_name}")
                next_evo_id = pokemon_chain_obj["evolves_to"][0]["species"]["url"].rstrip('/').split('/')[-1]
                self.evo_pokemon_id = next_evo_id


    
    def _find_next_evolution_name_and_id(self):
        if not self.evo_chain_dict:
            raise ValueError("No evolution chain object found!")
        if not self.pokemon_name:
            raise ValueError("Can't evolve the pokemon without having its name!")
        
        self._check_names_in_chain_recursive(self.evo_chain_dict)


    def evolve(self, pokemon_id: int):
        self.pokemon_id = pokemon_id
        self._get_name_and_evolution_chain_url_by_pokemon_id()
        self._get_evolution_chain_object()

        result = self._find_next_evolution_name_and_id()

        if not result:
            return (self.pokemon_name, )
        return (self.pokemon_name, result[0], result[1])
    
    def get_evolve_name(self):
        return self.evo_pokemon_name
    
    def get_evolve_id(self):
        return self.evo_pokemon_id




if __name__ == "__main__":
    print("executing")
    evo = Evolve()
    evo.evolve(17)

    print(evo.evo_pokemon_id)
    print(evo.evo_pokemon_name)

