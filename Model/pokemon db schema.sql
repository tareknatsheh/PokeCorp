CREATE DATABASE pokemon;

USE pokemon;

DROP TABLE IF EXISTS pokemons;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS pokemon_trainers;

CREATE TABLE pokemons(
	id INT PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	type VARCHAR(50),
	height INT,
	weight INT
);

CREATE TABLE trainers(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    town VARCHAR(50)
);

CREATE TABLE pokemon_trainers(
    pokemon_id INT,
    trainer_id INT,
    PRIMARY KEY (pokemon_id, trainer_id),
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE CASCADE
);

