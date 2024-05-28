import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from decouple import config
from Model.Entities import Pokemon
from typing import Optional
from Model.utils.db_error_handler import handle_database_errors

class MySql_repo:
    def __init__(self):
        self.db_password: str = str(config("SQL_DB_PASSWORD"))
        self.db_connection: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    @handle_database_errors
    def get_pokemon_by_id(self, id) -> Optional[Pokemon]:
        query = "SELECT id, name, height, weight FROM pokemons WHERE id = %s"

        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if not result:
            return None

        # Now the types of this pokemon:
        query = "SELECT pokemon_id, type FROM types WHERE pokemon_id = %s"
        self.cursor.execute(query, (id,))
        all_types = self.cursor.fetchall()
        all_types = [t[1] for t in all_types]
        print(all_types)
        return Pokemon(id=result[0], name=result[1], height=result[2], weight=result[3], type=all_types)

    @handle_database_errors
    def add_new_pokemon(self, new_pok: Pokemon):
        # First, add to pokemons table
        query = "INSERT INTO pokemons (id, name, height, weight) VALUES (%s, %s, %s, %s)"

        if not self.cursor:
            raise Exception("cursor not initialized")
        
        if not self.db_connection:
            raise Exception("cursor not initialized")
        
        values = (new_pok.id, new_pok.name, new_pok.height, new_pok.weight)
        self.cursor.execute(query, values)
        self.db_connection.commit()

        # Then, add to types table:
        if not len(new_pok.type) == 0:
            for t in new_pok.type:
                query = "INSERT INTO types (pokemon_id, type) VALUES (%s, %s)"
                values = (new_pok.id, t)

                self.cursor.execute(query, values)
                self.db_connection.commit()

        return new_pok
    
    @handle_database_errors
    def find_and_filter_type_trainer(self, type: Optional[str], trainer_name: Optional[str]) -> list[dict]:
        sql_query = """
            SELECT DISTINCT p.id, p.name, p.height, p.weight
            FROM pokemons p
            LEFT JOIN types t ON p.id = t.pokemon_id
            LEFT JOIN pokemon_trainers pt ON p.id = pt.pokemon_id
            LEFT JOIN trainers tr ON pt.trainer_id = tr.id
            WHERE (t.type = %s OR %s IS NULL)
            AND (tr.name = %s OR %s IS NULL);
        """

        if not self.cursor:
            raise Exception("cursor not initialized")
        
        self.cursor.execute(sql_query, (type, type, trainer_name, trainer_name))
        result = self.cursor.fetchall()
        result = [{"id": p[0], "name": p[1], "height": p[2], "weight": p[3]} for p in result]
        return result

    
    def _connect(self):
        print("connecting to db ......")
        self.db_connection = pymysql.connect(
            host="localhost",
            user="root",
            password=self.db_password,
            database="pokemon"
        )
        self.cursor = self.db_connection.cursor()
    
    def _close(self):
        if self.cursor:
            self.cursor.close()
        if self.db_connection:
            self.db_connection.close()


if __name__ == "__main__":
    # Sanity checking the DB repo
    mysql = MySql_repo()
    a_pok = mysql.get_pokemon_by_id(34)
    print(a_pok)
        
    