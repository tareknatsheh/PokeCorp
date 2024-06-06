from Model.DB_Interface import DB_Interface
from Model.Repositories import Pokemon_Repo, Trainer_Repo
from tests.testing_db_implementation import Testing_repo

class Database:
    def __init__(self):
        self.my_db: DB_Interface = Testing_repo()
        self.pokemon = Pokemon_Repo(self.my_db)
        self.trainer = Trainer_Repo(self.my_db)
        pass

def create_database() -> Database:
    return Database()