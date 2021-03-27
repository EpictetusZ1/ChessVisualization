DELIMITER $$

CREATE TRIGGER update_moves
AFTER INSERT
ON game FOR EACH ROW
BEGIN
  INSERT chessdata.all_game_moves(game_ID, moves)
  SELECT game_ID, moves FROM game
  WHERE game_ID IN (SELECT MAX(game_ID) FROM game);
END$$

DELIMITER ;
