import PgnParsing as PgnDf
import re
import pandas as pd
from collections import Counter


games = PgnDf.get_all_game_data()


def separate_moves(text):
    move_counter = 0.5
    ply_counter = 1
    base_text = str(text)
    pattern = re.compile(r"([0-9]+\.|[0-9]+\.\s)(((O-O\sO-O\s)|[^O]\w*.\s[^O]\w*.\s)|([^O]\w*.\s(O-O\s))|"
                         r"(O-O\s[^O]\w*.)|([^O]\w*.\sO-O-O\s)|(O-O-O\s[^O]\w*.\s)|(O-O-O\sO-O-O\s)|(O-O\sO-O-O\s)|"
                         r"(O-O-O\sO-O\s)|(\w*.\s.+-.+)|(\w*=\w\s\w*)|(\w*\s\w*=\w\s))")
    matches = pattern.finditer(base_text)
    ply_ls = []

    for match in matches:
        move = match.group(0)
        # Splitting a ply into two "moves" then appending the first value(white) and the second(black)
        move = move.split(" ")
        ply_ls.append(move[1])
        move_counter += 0.5
        ply_ls.append(move[2])
        ply_counter += 1

    # print(ply_ls)
    return ply_ls


games["clean_tokenized"] = games["moves"].apply(lambda x: separate_moves(x))

# print(games.info())
# games.to_csv('games_test_data_set.csv')
# print(games)
# games.reset_index(drop=True)
column_avg = games["game_length"].mean()

print("The average amount of moves for games in this database= ", column_avg)

move_list_test = games.iat[0, 9]

c = Counter(move_list_test)

"""
Function used to count the freq of moves for the 'Clean Tokenized' column.
"""


def counter(text):
    cnt = Counter()
    for moves in text:
        for move in moves:
            cnt[move] += 1
    return cnt


text_cnt = counter(games["clean_tokenized"])

common_moves = text_cnt.most_common(30)
common_moves = pd.DataFrame(common_moves, columns=["moves", "counts"])

"""
Find the longest game in dataset.
"""


def find_max_list(lst):
    list_len = [len(i) for i in lst]
    max_game_length = max(list_len)
    # print(max(list_len))
    return max_game_length


"""
Separate ply moves into df containing 1 move(inside ply)
"""


def moves_individualized(games):
    ind_moves = []
    move_data = games["clean_tokenized"]
    longest_game = find_max_list(move_data)
    for item in move_data:  # Appending a placeholder value to smooth out jagged data
        if len(item) != longest_game:
            diff = longest_game - len(item)
            for i in range(diff):
                item.append("NONE")
        move_list = item
        ind_moves.append(move_list)
    return ind_moves


lists = moves_individualized(games)
df = pd.DataFrame(data=lists)

"""
Code below produces desired result (at most basic level). The function following tries to interpret data in 
a more efficient and desireable way.
"""

# print(df.shape)
# print(df.describe())
# print(df.groupby([0, 1]).size())

mve_cnt = 0


def get_freq_data(move_count):
    # df = dataframe.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    freq_of_move = df[move_count].value_counts().head(5).tolist()
    # print(freq_of_move)
    values = df[move_count].value_counts().head(5).keys().tolist()
    values = pd.Series(values)
    first_move_data = list(zip(values, freq_of_move))
    # print(first_move_data)
    for i in values:
        j = str(i)
        common_reply = df.groupby(move_count)
        freq_series = common_reply.get_group(j).value_counts().head(5)
        print(freq_series.unstack())


get_freq_data(mve_cnt)

