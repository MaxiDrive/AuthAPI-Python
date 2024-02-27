class Person():
    def __init__(self, Id_person, Name, Address, Mail, type_user_Id_type_user) -> None:
        self.Id_person=Id_person
        self.Name=Name
        self.Address=Address
        self.Mail=Mail
        self.type_user_Id_type_user=type_user_Id_type_user

    def to_JSON(self):
        return{
            'Id_person': self.Id_person,
            'Name': self.Name,
            'Address': self.Address,
            'Mail': self.Mail,
            'type_user_Id_type_user': self.type_user_Id_type_user
        }