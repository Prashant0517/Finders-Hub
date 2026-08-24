import sqlite3 as sq
con= sq.connect("mywebsite.db")
c=con.cursor()
c.execute("create table IF NOT EXISTS student(id INTEGER PRIMARY KEY AUTOINCREMENT,fullname varchar(100),mail varchar(50),pass varchar(20),contact INTEGER(10))")
c.execute("CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,post_type TEXT NOT NULL,item_name TEXT NOT NULL,description TEXT,category TEXT,location TEXT,date TEXT,contact TEXT,image TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES student(id))")
c.execute("ALTER TABLE posts DROP COLUMN image")
con.commit()
con.close()