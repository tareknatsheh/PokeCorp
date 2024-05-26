def read_json_file(file_path: str) -> list[dict]:
    with open(file_path) as f:
        data = json.load(f)
        if not data:
            raise ValueError(f"There is no data in the provided file: {file_path}")
        return data

def from_list_to_str(a_list: list[str]) -> str:
    result = ""
    for item in a_list:
        if len(result) == 0:
            result += f"{item}"
        else:
            result += f", {item}"
    return result

def migrate_pokemons_table(conn, data: list):
    cursor = conn.cursor()
    for pokemon in data:
        pokemon_types_str = ', '.join(pokemon["type"])
        query = "INSERT INTO pokemons (id, name, type, height, weight) VALUES (%s, %s, %s, %s, %s)"
        values = (pokemon["id"], pokemon["name"], pokemon_types_str, pokemon["height"], pokemon["weight"])
        cursor.execute(query, values)
        conn.commit()

def db_init():
    db_password: str = config("SQL_DB_PASSWORD")
    db_con = pymysql.connect(host="localhost", user="root", password=db_password, database="pokemon")
    return db_con


def main():
    json_file_path = "./Model/pokemons_data.json"

    connection = db_init()
    json_data = read_json_file(json_file_path)
    migrate_pokemons_table(connection, json_data)

    connection.close()

if __name__ == "__main__":
    import pymysql
    from decouple import config
    import json

    main()