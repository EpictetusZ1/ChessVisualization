# Chess Visualization and Database


#### *A program that lets you discover and visualize candidate moves*



### Features:

##### PGN Extractor:

  - Parser can handle both individual game files, and pgn files that contain multiple games.
      - Currently can only deal with limited tag values (Not "time", "comments" - which are generated automatically from most online games)
  - PGN parser to filter game *tag* values (i.e. [Black  "Famous Chess Player Name"]) then add values to a data.

  - Parse each individual move from the pgn file and add list of the individualized moves to the same data frame (similar to word tokenization).


##### Database:
  - Sql files for creation of database tables (RDBM: MySql).
  - Triggers to populate a separate *moves* table (needed for visualization).
  - Connect database to python for data manipulation.
  - Example input and query.


##### Visualization:
  - Can show frequency of most popular "first" move for games in the database
    - (Note: a move is one individual player action, two "moves" result in a "ply" or "turn" being completed)

  - Show "second" move frequency as a dependant of the first move. Which in turn gives us a list of the most frequently occurring the next move for each instance of move.
    - This is still being worked on, the end goal is to show them on the board, in a Seaborn heat map sort of way with the top 3 replies to each move being displayed.


### Current Status:
- Still working through the multi-index problem of yielding top 3 most popular moves from database (children) from the desired index move (parent). Need to add ability to select a given move index and evaluate if the previous moves == any in database, then provide popular moves based off existence of that unique sequence of moves in database games.


#### About this data:
- Sample data is 88 games. Can be viewed in '/games' dir.
- 155 is the length of 'moves' of the longest game in the data frame (Note: there is 2 moves in a 'ply', the longest game has 78 plys).
- All games have been appended with 'None' string values to make the data non-jagged.
- Column[0] contains whites 5 most popular first moves (d4, e4, c4, Nf3).
- Column[1] contains blacks 3 most common replies to each [0] move from white.


![Current output](Assets/Output_ChessV.png?)


#### To be added:
- Web scraper
  -  To download Master chess games (".pgn" files) from a unnamed-popular-chess-website and populate database with results.
