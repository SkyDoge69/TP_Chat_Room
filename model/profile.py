# from database import SQLite
# from errors import ApplicationError
 
# class Profile(object):
 
#     def __init__(self, username, description, profile_id = None):
#         self.id = profile_id
#         self.username = username
#         self.description = description
 
#     def to_dict(self):
#         profile_data = self.__dict__
#         return profile_data
 
#     def save(self):
#         with SQLite() as db:
#             cursor = db.execute(self.__get_save_query())
#             self.id = cursor.lastrowid
#         return self

#     @staticmethod
#     def get_description(username):
#         with SQLite() as db:
#             result = db.execute(
#                 "SELECT description FROM profiles WHERE username = ?",
#                 (username))
#             profile = result.fetchone()
#         return ''.join(profile[0]) 


#     @staticmethod
#     def all():
#         with SQLite() as db:
#             result = db.execute(
#                     "SELECT username, description, id FROM profiles").fetchall()
#             return [Profile(*row) for row in result]
 
#     def __get_save_query(self):
#         query = "{} INTO profiles {} VALUES {}"
#         if self.id == None:
#             args = (self.username, self.description)
#             query = query.format("INSERT", "(username, description)", args)
#         else:
#             args = (self.id, self.username, self.description)
#             query = query.format("REPLACE", "(id, username, description)", args)
#         return query