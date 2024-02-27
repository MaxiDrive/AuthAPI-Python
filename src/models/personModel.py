from database.db import get_connection
from .entities.person import Person


class PersonModel():

    @classmethod
    def get_person(cls):
        try:
            connection = get_connection()
            person_list = []

            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM person')
                result_set = cursor.fetchall()

                for row in result_set:
                    person = Person(row[0], row[1], row[2], row[3], row[4])
                    person_list.append(person.to_JSON())

            connection.close()
            return person_list

        except Exception as ex:
            raise Exception(str(ex))
