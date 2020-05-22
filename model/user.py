from database import SQLite
from errors import ApplicationError
from flask_login import UserMixin

class User(UserMixin):
 
    def __init__(self, name, password, room, description, picture_location, user_id=None):
        self.id = user_id
        self.name = name
        self.password = password
        self.room = room
        self.description = description
        self.picture_location = picture_location
 
    def to_dict(self):
        user_data = self.__dict__
        return user_data

    def to_viewable(self):
        user_data = self.__dict__
        del user_data["password"]
        return user_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self
 
    @staticmethod
    def delete(user_id):
        result = None
        with SQLite() as db:
            result = db.execute("DELETE FROM user WHERE id = ?",
                    (user_id,))
        if result.rowcount == 0:
            raise ApplicationError("No value present", 404)
 
    @staticmethod
    def find(user_id):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, room, description, picture_location, id FROM user WHERE id = ?",
                    (user_id,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "User with id {} not found".format(user_id), 404)
        return User(*user)
 
    @staticmethod
    def find_by_name(name):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, room, description, picture_location, id FROM user WHERE name = ?",
                    (name,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "User with name {} not found".format(name), 404)
        return User(*user)
 
 
    @staticmethod
    def update_room(room, name):
        result = None
        with SQLite() as db:
            result = db.execute("UPDATE user SET room = ? WHERE name = ?",
                    (room, name))
        if result.rowcount == 0:
            raise ApplicationError("No user present", 404)
 
    @staticmethod
    def find_user_password(username, password):
        result = None
        with SQLite() as db:
            result = db.execute("SELECT * FROM user WHERE name = ? and password = ?",
                    (username, password))
            check = result.fetchone()
            if check is None:
                return False
            else:
                return True


    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, room, description, picture_location, id FROM user").fetchall()
            return [User(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.id == None:
            args = (self.name, self.password, self.room, self.description, self.picture_location)
            query = query.format("INSERT", "(name, password, room, description, picture_location)", args)
        else:
            args = (self.id, self.name, self.password, self.room, self.description, self.picture_location)
            query = query.format("REPLACE", "(id, name, password, room, description, picture_location)", args)
        return query