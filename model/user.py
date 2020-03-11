from database import SQLite
from errors import ApplicationError


class User(object):

    def __init__(self, name, password, user_id=None):
        self.id = user_id
        self.name = name
        self.password = password
      
      
    def to_dict(self):
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
                    "SELECT name, password, id FROM user WHERE id = ?",
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
                    "SELECT name, password, id FROM user WHERE name = ?",
                    (name,))
        user = result.fetchone()
        if user is None:
            raise ApplicationError(
                    "User with name {} not found".format(name), 404)
        return User(*user)

    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT name, password, id FROM user").fetchall()
            return [User(*row) for row in result]

    def __get_save_query(self):
        query = "{} INTO user {} VALUES {}"
        if self.id == None:
            args = (self.name, self.password)
            query = query.format("INSERT", "(name, password)", args)
        else:
            args = (self.id, self.name, self.password)
            query = query.format("REPLACE", "(id, name, password)", args)
        return query
