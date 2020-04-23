import sqlite3 as sqlite


DB_NAME = "example.db"

conn = sqlite.connect(DB_NAME)

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS user
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        room STRING,
        FOREIGN KEY(room) REFERENCES rooms(name)
    )
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS rooms
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        is_private INTEGER,
        name STRING
    )
''')
conn.commit()

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS invites
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_name STRING,
        username STRING
    )
''')
conn.commit()

# conn.cursor().execute('''
# CREATE TABLE IF NOT EXISTS profiles
#     (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username STRING,
#         description TEXT NOT NULL
#     )
# ''')
# conn.commit()

# SELECT * FROM ime WHERE room_id = ? and username = ?", (id, name)
# SELECT * FROM ime WHERE room_id = ?, 


#conn.cursor().execute('''
#CREATE TABLE IF NOT EXISTS ad
#   (
#        id INTEGER PRIMARY KEY AUTOINCREMENT,
#        title TEXT,
#        content TEXT,
#        price INTEGER,
#        release_date TEXT,
#        is_active INTEGER,
#        creator_id INTEGER,
#        buyer_id INTEGER,
#        FOREIGN KEY(creator_id) REFERENCES user(id),
#        FOREIGN KEY(buyer_id) REFERENCES user(id)
#    )
#''')
#conn.commit()


class SQLite(object):

    def __enter__(self):
        self.conn = sqlite.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()

