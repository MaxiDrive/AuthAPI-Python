from database.db import get_connection
from .entities.users import Users


class UserModel():

    @classmethod
    def get_users(cls):
        try:
            connection = get_connection()
            users_list = []

            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM login')
                result_set = cursor.fetchall()

                for row in result_set:
                    user = Users(row[0], row[1], row[2], row[3])
                    users_list.append(user.to_JSON())

            connection.close()
            return users_list

        except Exception as ex:
            raise Exception(str(ex))
