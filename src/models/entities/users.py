class Users():
    def __init__(self, Id_login, User, Password, person_Id_person) -> None:
        self.Id_login=Id_login
        self.User=User
        self.Password=Password
        self.person_Id_person=person_Id_person

    def to_JSON(self):
        return{
            'Id_login': self.Id_login,
            'User': self.User,
            'Passwors': self.Password,
            'person_Id_person': self.person_Id_person
        }