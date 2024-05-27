import pymysql
from decouple import config
from Entities import Pokemon
from typing import Optional


class MySql_repo:
    def __init__(self):
        db_password: str = str(config("SQL_DB_PASSWORD"))
        self.db_connection = pymysql.connect(
            host="localhost",
            user="root",
            password=db_password,
            database="pokemon"
        )
        self.cursor = self.db_connection.cursor()

    def get_sql_version(self):
        """Get SQL version (used just for sanity check)

        Returns:
            str: X.X.X sql version number
        """
        try:
            self.cursor.execute("SELECT VERSION()")
            result = self.cursor.fetchone()
            if not result:
                return None
            
            return result[0]
        except pymysql.Error as e:
            print(f"There was an error with db in get_sql_version(): {e}")
        finally:
            self.db_connection.close()
    
    def get_pokemon_by_id(self, id) -> Optional[Pokemon]:
        query = "SELECT id, name, type, height, weight FROM pokemons WHERE id = %s"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if not result:
            return None
        return Pokemon(result[0], result[1], result[2], result[3], result[4])


if __name__ == "__main__":
    mysql = MySql_repo()
    sql_ver = mysql.get_sql_version()
    print(sql_ver)

    a_pok = mysql.get_pokemon_by_id(34)
    print(a_pok)
        
    