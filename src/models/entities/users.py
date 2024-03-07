class Users:
    def __init__(self, Id_person, Name, Address, Mail, UserName, Password, Age, Img) -> None:
        self.Id_person = Id_person
        self.Name = Name
        self.Address = Address
        self.Mail = Mail
        self.UserName = UserName
        self.Password = Password
        self.Age = Age
        self.Img = Img

    def to_JSON(self):
        return {
            'Id_person': self.Id_person,
            'Name': self.Name,
            'Address': self.Address,
            'Mail': self.Mail,
            'UserName': self.UserName,
            'Password': self.Password,
            'Age': self.Age,
            'Img': self.Img
        }
