import re
import os
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

pd.options.display.max_rows = 999

start = "\033[1m"
end = "\033[0;0m"

"""
Create dataframe from Dict list, after iterating through dir of files and appending data to dict.
"""


def get_all_game_data():
    for path, dirs, files in os.walk("games"):
        dict_list = []
        keys = ["event", "site", "date", "round_num", "white", "black", "result", "game_length", "moves"]
        for f in files:
            file_name = os.path.join(path, f)
            byte_size = os.path.getsize(file_name)
            if byte_size >= 2501:
                with open(file_name, "r", encoding="utf-8", errors="ignore") as my_file:
                    string = my_file.read()

                    string = re.sub(r'\""', r'"?"', string)

                    multi_pgn_get_all_game_data(string, dict_list)

            else:
                with open(file_name, "r") as my_file:
                    # print("\n" + start + os.path.basename(file_name) + end, byte_size)
                    string = my_file.read()
                    all_tags = tags_to_list(string)
                    # print(moves_to_list(string))
                    # ---- This returns a list of the moves in the format for structuring the data properly
                    all_moves, game_len = moves_to_list(string)

                data_dict = {keys: all_tags for keys, all_tags in zip(keys, all_tags)}
                data_dict["game_length"] = game_len
                data_dict["moves"] = all_moves
                dict_list.append(data_dict)
        data_frame_games = pd.DataFrame(dict_list)

        data_frame_games.insert(0, "game_ID", 0)

        data_frame_games = data_frame_games[["game_ID", "event", "site", "date", "round_num",
                                             "white", "black", "result", "game_length", "moves"]].set_index("game_ID")

        return data_frame_games


"""
Parse string file for a list of their tag elements ( i.e. [Site Paris(France)] )
"""


def tags_to_list(string):
    pattern_tags = re.compile(r"\"(.+)\"")
    match_tags = pattern_tags.finditer(string)
    tag_list = []
    for match_tag in match_tags:
        tag_list.append(match_tag.group(1))
    return tag_list


"""
Takes a move list "1. e4 e5 , 2.Nf3 Nc6" and converts it to one string object --> "1. ef e5 2. Nf3 Nf6"
"""


def convert_list_to_string(move_list, separator="  "):

    return separator.join(move_list)


"""
Parse string to return all the move elements as list
(separate from tags - important for Database functionality)
"""


def moves_to_list(string):
    string = string.replace("\n", " ")

    pattern = re.compile(r"[0-9]+\.\s(((O-O\sO-O\s)|[^O]\w*.\s[^O]\w*.\s)|([^O]\w*.\s(O-O\s))|(O-O\s[^O]\w*.)|"
                         r"([^O]\w*.\sO-O-O\s)|(O-O-O\s[^O]\w*.\s)|(O-O-O\sO-O-O\s)|(O-O\sO-O-O\s)|"
                         r"(O-O-O\sO-O\s)|(\w*.\s.+-.+)|(\w*=\w\s\w*)|(\w*\s\w*=\w\s))")
    matches = pattern.finditer(string)
    move_list = []
    for match in matches:
        move_list.append(match.group())
    game_length = (len(move_list))
    return convert_list_to_string(move_list), game_length


"""
Going to have to write a function that checks if there is a newline at the end of the file 
"""


def line_checker():
    with open("/Users/jackheaton/PycharmProjects/Chess/Chess/games/master_games.pgn", "a") as my_file:
        my_file.write("\n\n\n")
    pass




"""
Separates a file full of games into list elements that each contain an individual game 
"""


def multi_game_pgn_filter(string):
    game_list = []
    pat1 = re.compile(r"\n(?s).*?(?=\n\n\n)")
    games = pat1.findall(string)

    for game in games:

        game_list.append(game)
        # print(game, sep='\n')
    return game_list


"""
Get all data from individual games, append to dict then write to dataframe
"""


def multi_pgn_get_all_game_data(my_file, dict_list):
    keys = ["event", "site", "date", "round_num", "white", "black", "result", "game_length", "moves"]
    games = multi_game_pgn_filter(my_file)

    for game in games:

        all_tags = multi_pgn_tags_to_list(game)
        moves, game_len = multi_pgn_moves_to_list(game)
        # print(tags, moves)
        data_dict = {keys: all_tags for keys, all_tags in zip(keys, all_tags)}
        data_dict["game_length"] = game_len
        data_dict["moves"] = moves
        dict_list.append(data_dict)

    multi_game_dataframe = pd.DataFrame(dict_list)
    multi_game_dataframe.insert(0, "game_ID", 0)
    multi_game_dataframe = multi_game_dataframe[["game_ID", "event", "site", "date", "round_num",
                                                 "white", "black", "result", "game_length",
                                                 "moves"]].set_index("game_ID")
    return multi_game_dataframe


"""
Parse string file for a list of their tag elements ( i.e. [Site Paris(France)] )
"""


def multi_pgn_tags_to_list(game):
    game = game.replace("\\n", " ")
    pattern_tags = re.compile(r"\"(.+)\"")
    matches = pattern_tags.finditer(game)
    tags = []
    for match_tag in matches:
        tags.append(match_tag.group(1))
    return tags


"""
Parse string to return all the move elements as list
(separate from tags - important for Database functionality)
"""


def multi_pgn_moves_to_list(game):
    game = game.replace("\n", " ")
    game = re.sub(r"(\{.%.\w*\s\d:\d\d:\d\d\]\}\s\s)", "", game)
    game = re.sub(r"(\d\.)([a-z]|[A-Z])", r"\1 \2", game)  # Formatting string --> add space between ply count and move
    pattern = re.compile(r"([0-9]+\.|[0-9]+\.\s)(((O-O\sO-O\s)|[^O]\w*.\s[^O]\w*.\s)|([^O]\w*.\s(O-O\s))|"
                         r"(O-O\s[^O]\w*.)|([^O]\w*.\sO-O-O\s)|(O-O-O\s[^O]\w*.\s)|(O-O-O\sO-O-O\s)|(O-O\sO-O-O\s)|"
                         r"(O-O-O\sO-O\s)|(\w*.\s.+-.+)|(\w*=\w\s\w*)|(\w*\s\w*=\w\s))")
    matches = pattern.finditer(game)
    moves_ls = []
    for match in matches:
        moves_ls.append(match.group(0))
    game_length = (len(moves_ls))
    return convert_list_to_string(move_list=moves_ls), game_length


get_all_game_data()




