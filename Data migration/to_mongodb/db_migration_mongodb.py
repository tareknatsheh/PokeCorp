from pymongo.collection import Collection

def db_init() -> Collection:
    client: MongoClient = MongoClient("mongodb://localhost:5003/")
    cursor = client["PokeCorpDB"]
    collection = cursor["Pokemons"]
    return collection

def add_all(collection: Collection, pokemons: list[dict]):
    collection.insert_many(pokemons)


def read_json_file(file_path: str) -> list[dict]:
    with open(file_path) as f:
        data = json.load(f)
        if not data:
            raise ValueError(f"There is no data in the provided file: {file_path}")
        return data


def main():
    json_file_path = "D:/backend-bootcamp/Final project/PokeCorp/Data migration/data seed/pokemons_data.json"

    collection = db_init()
    json_data = read_json_file(json_file_path)

    add_all(collection, json_data)


if __name__ == "__main__":
    from pymongo import MongoClient
    import json

    main()