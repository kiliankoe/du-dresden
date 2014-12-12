import sqlite3 as db

con = db.connect('data.db')

with con:
    cur = con.cursor()
    cur.execute('CREATE TABLE "Twitter" ('
                '"id" INTEGER NOT NULL ON CONFLICT FAIL PRIMARY KEY UNIQUE ON CONFLICT FAIL,'
                '"status" TEXT NOT NULL'
                ');')

cur.close()
con.close()
