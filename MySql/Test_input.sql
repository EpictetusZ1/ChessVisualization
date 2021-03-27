-- COL Order:
--    game_id (auto increment), game_name, event, date, site,
--    white, black, result, game_length(int), moves VARHCAR(3000)
INSERT INTO game VALUES(0, 'Morphy vs. Anderssen', 'Match','Paris (France)',
'1858.??.??', 'Paul Morphy', 'Adolf Anderssen', '1-0', 17,
'1. e4 c5 2. d4 cxd4 3. Nf3 Nc6 4. Nxd4 e6 5. Nb5 d6 6. Bf4 e5 7. Be3 f5 8. N1c3
 f4 9. Nd5 fxe3 10. Nbc7+ Kf7 11. Qf3+ Nf6 12. Bc4 Nd4 13. Nxf6+ d5 14. Bxd5+ Kg6
 15. Qh5+ Kxf6 16. fxe3 Nxc2+ 17. Ke2 1-0');


-- EXAMPLE QUERY: This selects all games where Bobby Fischer played with the
-- black pieces and he played the Sicilian Defense

SELECT * FROM game
WHERE game.black = "Bobby Fischer"
AND game.moves LIKE "%1. e4 c5%" ;
