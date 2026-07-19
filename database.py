import sqlite3 as sq
con= sq.connect("mydata1.db")
c=con.cursor()
c.execute("create table student(id INTEGER PRIMARY KEY AUTOINCREMENT,fullname varchar(100),mail varchar(50),pass varchar(20),contact integer(10)")
con.commit()
con.close()