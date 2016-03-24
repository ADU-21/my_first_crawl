import sqlite3
db_name = r'test'

con = sqlite3.connect(db_name)
cur = con.cursor()
cur.execute('CREATE TABLE TABLE_NAME (),')
cur.execute('SELECTE * FROM　TABEL_NAME WHERE ...')
cur.execute('INSERT INTO TABLE_NAME (..)VALUES (?),(..)')
date_set = cur.fetchall()
for row in date_set:
  print(row)
cur.close()
con.cloes()