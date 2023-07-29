import sqlite3
con = sqlite3.connect('instance/db.sqlite')
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS QuestionList")
print(cur.fetchall())
