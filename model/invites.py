from database import SQLite
from errors import ApplicationError
 
class Invite(object):
 
    def __init__(self, room_name, username, invite_id = None):
        self.id = invite_id
        self.room_name = room_name
        self.username = username
 
    def to_dict(self):
        invite_data = self.__dict__
        return invite_data
 
    def save(self):
        with SQLite() as db:
            cursor = db.execute(self.__get_save_query())
            self.id = cursor.lastrowid
        return self



    @staticmethod
    def find_by_room(room_name):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT room_name, username, id FROM invites WHERE room_name = ?",
                    (room_name,))
        invite = result.fetchone()
        if invite is None:
            raise ApplicationError(
                    "Invite for room {} not found".format(room_name), 404)
        return Invite(*invite)
 
    @staticmethod
    def add_invite(room_name, username):
        with SQLite() as db:
            result = db.execute(
                    "INSERT INTO invites(room_name, username) VALUES (?, ?)",
                    (room_name, username))
            invite = result.fetchone()
        # if invite is None:
        #     raise ApplicationError(
        #             "Invite for room {} not found".format(room_name), 404)
        #return Invite(*invite)
    
    @staticmethod
    def check_for_invite(room_name, username):
        result = None
        with SQLite() as db:
            result = db.execute(
                    "SELECT * FROM invites WHERE room_name = ? AND username = ?",
                    (room_name, username))
        invite = result.fetchone()
        if invite is not None:
            return True
        return False

    @staticmethod
    def all():
        with SQLite() as db:
            result = db.execute(
                    "SELECT room_name, username, id FROM invites").fetchall()
            return [Invite(*row) for row in result]
 
    def __get_save_query(self):
        query = "{} INTO invites {} VALUES {}"
        if self.id == None:
            args = (self.room_name, self.username)
            query = query.format("INSERT", "(room_name, username)", args)
        else:
            args = (self.id, self.room_name, self.username)
            query = query.format("REPLACE", "(id, room_name, username)", args)
        return query