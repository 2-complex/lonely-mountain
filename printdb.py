import sqlite3
conn = sqlite3.connect('testing.db')
c = conn.cursor()
r = c.execute('SELECT * FROM files')
l = r.fetchall()
for x in l:
    print x


