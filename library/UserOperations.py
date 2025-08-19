from User import User
import re
from tabulate import tabulate
import phonenumbers
from phonenumbers import geocoder
from Library_main import Library

class UserOperations(Library):
    def __init__(self):
        super().__init__()


    def user_input(self):
        while True:
            print('1-Register a user\n2-List current users\n3-Exit')
            user = input()
            if user == '1':
                self.register_user()
            elif user == '2':
                self.list_users()
            elif user == '3':
                return user
            else:
                print('Invalid input!')


    def input_processing(self, order, input_value,exist_users):

            if order == 'name': #Motasem105_w
                check_name = re.search(r'^[A-Za-z]{1,}[0-9]*\s?_?[A-Za-z0-9]*\s?_?[A-Za-z1-9]*$', input_value)
                if not check_name:
                    print('The format of the name is not correct!')
                    return
                if input_value in [ele[1] for ele in exist_users]:
                        print('The name is already exist!')
                        return
                return input_value

            elif order == 'email':
                check_email = re.search(r'^[a-zA-Z0-9]+([._%+-][a-zA-Z0-9]+)*@(gmail|yahoo|example)\.com', input_value)
                if not check_email:
                    print('The format of the email is not correct!')
                    return
                if input_value in [ele[2] for ele in exist_users]:
                    print('The email is already exist!')
                    return
                return input_value

            elif order == 'phone number':

                valid_candidates = []
                for region in phonenumbers.SUPPORTED_REGIONS:
                    try:
                        num = phonenumbers.parse(input_value, region)
                        if phonenumbers.is_valid_number(num):
                            valid_candidates.append((region, geocoder.description_for_number(num, "en")))
                    except phonenumbers.NumberParseException:
                        continue
                if not valid_candidates:
                    print('Invalid phone number!')
                    return

                if input_value in [ele[3] for ele in exist_users]:
                    print('the phone is already exist!')
                    return
                return input_value

    def register_user(self):
        exist_users = self.dataBase.fitch('all_rows', 'users')
        while True:

            name = input('Enter a name: ').strip()
            if not self.input_processing('name', name, exist_users):
                continue
            break

        while True:
            email = input('Enter an email: ').strip()
            if not self.input_processing('email', email, exist_users):
                continue
            break

        while True:
            phone_number = input('Enter a phone number: ').strip()
            if not self.input_processing('phone number', phone_number, exist_users):
                continue
            break

        ida = self.dataBase.control('create_id', 'users')
        user = User(ida, name, email, phone_number)
        self.dataBase.control('add', user)

    def list_users(self):
        all_users = self.dataBase.fitch('all_table', 'users')
        if not all_users:
            print('There are any users in dataBase.')
            return
        print(tabulate(all_users , 'keys'))


