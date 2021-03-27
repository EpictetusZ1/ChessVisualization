CREATE TABLE all_game_moves (
    game_ID INT(11),
    moves VARCHAR(5000)
);

DESCRIBE all_game_moves;

ALTER TABLE all_game_moves ADD PRIMARY KEY(game_ID);

ALTER TABLE all_game_moves ADD FOREIGN KEY(game_ID)
REFERENCES game(game_ID)
ON DELETE CASCADE;


CREATE TABLE game (
    game_ID INT(11),
    game_name VARCHAR(150),
    event VARCHAR(32),
    site VARCHAR(32),
    date VARCHAR(10),
    round_num VARCHAR(4),
    white VARCHAR(32),
    black VARCHAR(32),
    result VARCHAR(10),
    game_length INT NOT NULL DEFAULT '0',
    moves VARCHAR(5000)
);

ALTER TABLE game ADD PRIMARY KEY(game_ID);
ALTER TABLE game MODIFY game_ID INT(11) AUTO_INCREMENT;

-- Reset the auto_increment when testing inputs for database
-- ALTER TABLE game auto_increment = 1;

--ALTER TABLE all_game_moves auto_increment = 1;
