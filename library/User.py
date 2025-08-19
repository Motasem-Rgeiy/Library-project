
class User:

    def __init__(self,id, name, email, phone_number):
        self.id = id
        self.name = name
        self.email = email
        self.phone_number = phone_number

    def __str__(self):
        return f'{self.id}, {self.name}, {self.email}, {self.phone_number}'

    def __eq__(self, other):
        if self.name == other.name:
            print('The name is already exist!')
            return True
        if self.email == other.email:
            print('The email is already exist!')
            return True
        if self.phone_number == other.phone_number:
            print('The phone number is already exist!')
            return True
        return
