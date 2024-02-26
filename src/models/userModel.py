from database.db import get_connection
from .entities.user import user

class userModel():
    
    @classmethod
    def get_users(self):
        try:
            connection=get_connection()
            users=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM login")
                resultset = cursor.fetchall()

                for row in resultset:
                    users=users(row[0], row[1], row[2], row[3])
                    users.append(users.to_JSON())

            connection.close()
            return users

        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def get_user(self, id):
        try:
            connection=get_connection()
            user=[]

            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM login WHERE id = %s",(id,))
                row = cursor.fetchall()

                user=None
                if row != None:
                    user = user(row[0], row[1], row[2], row[3])
                    user = user.to_JSON()

            connection.close()
            return user

        except Exception as ex:
            raise Exception(ex)