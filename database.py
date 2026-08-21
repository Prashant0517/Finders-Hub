import sqlite3 as sq
con= sq.connect("mywebsite.db")
c=con.cursor()
c.execute("create table student(id INTEGER PRIMARY KEY AUTOINCREMENT,fullname varchar(100),mail varchar(50),pass varchar(20),contact INTEGER(10))")
con.commit()
con.close()