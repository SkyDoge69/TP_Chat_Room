from database import SQLite
from errors import ApplicationError
 
class Room(object):
 
    def __init__(self, is_private, name, room_id = None):
        self.id = room_id
        self.is_private = is_private
        self.name = name
 
    def to_dict(self):
        room_data = self.__dict__
        return room_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self

    @staticmethod
    def find_by_name(name):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT is_private, name, id FROM rooms WHERE name = ?",
                    (name,))
        room = result.fetchone()
        if room is None:
            raise ApplicationError(
                    "Room with name {} not found".format(name), 404)
        return Room(*room)
 
    @staticmethod
    def add_room(is_private, name):
        with SQLite() as db:
            result = db.execute(
                    "INSERT INTO rooms(is_private, name) VALUES (?, ?)",
                    (is_private, name))
            room = result.fetchone()
        # if room is None:
        #     raise ApplicationError(
        #             "Room with name {} not found".format(name), 404)
        # return Room(*room)
        
    @staticmethod
    def delete_room(name):
        with SQLite() as db:
            result = db.execute(
                    "DELETE FROM rooms WHERE name = ?",
                    (name,))
            room = result.fetchone()
        # if room is None:
        #     raise ApplicationError(
        #             "Room with name {} not found".format(name), 404)
        # return Room(*room)

    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT is_private, name, id FROM rooms").fetchall()
            return [Room(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO rooms {} VALUES {}"
        if self.id == None:
            args = (self.is_private, self.name)
            query = query.format("INSERT", "(is_private, name)", args)
        else:
            args = (self.id, self.is_private, self.name)
            query = query.format("REPLACE", "(id, is_private, name)", args)
        return query