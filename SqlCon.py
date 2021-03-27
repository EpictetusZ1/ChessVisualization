from Chess import PgnParsing as PgnDf
import sqlalchemy
import mysql.connector as sql

conn = sql.connect(host="localhost", user="root", password="<insert_password>", database="chessdata")

cursor = conn.cursor()

cursor.execute("SELECT * FROM game")

for x in cursor:
    print(x)

# cursor.execute("SET autocommit = 1")
# cursor.close()
# conn.close()

# df = PgnDf.get_all_game_data()
#
# db_engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:password@localhost:3306/chessdata')
#
#
# df.to_sql(name='game', con=db_engine, if_exists='append',  index=False)


