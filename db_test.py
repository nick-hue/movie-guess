import sqlite3

con = sqlite3.connect("tutorial.db")
cur = con.cursor()

# cur.execute("CREATE TABLE player(name, score)")




# cur.execute("""
#     INSERT INTO player VALUES
#         ('nikos', 1)
# """)

res = cur.execute("SELECT name FROM player")
print(res.fetchall())



