from datetime import datetime,timedelta
from datetime import date
from Borrow import Borrow
from tabulate import tabulate
from BookOperations import BookOperations
from Library_main import Library
from Autmoations import Automations

class BorrowReturn(Library):
    def __init__(self):
        self.auto = Automations()
        super().__init__()


    def user_input(self):
        message = """1-Borrow a book
2-Return a book
3-List Borrow/Return History
4-Exit"""
        while True:
            print(message)
            user = input().strip()
            if user == '1':
                self.borrow_book()
            elif user =='2':
                self.return_book()
            elif user == '3':
                self.display_control()
            elif user == '4':
                return user

            else:
                print('Invalid input!')


    def borrow_book(self):
        book_obj = BookOperations()
        book = book_obj.title_id('borrow' , 'books')
        if not book:
            return
        current_users = self.dataBase.fitch('all_rows' , 'users')
        if not current_users:
            print('There are no users in dataBase,register a user!')
            return

        user = input('Enter the name of the user: ')
        if not user in [current_user[1] for current_user in current_users]:
            print('the user is not exist! ')
            return

        start_date = str(date.today().strftime('%d-%m-%Y'))

        date_obj = datetime.strptime(start_date, "%d-%m-%Y")

        new_date = date_obj + timedelta(days=7)
        due_date = new_date.strftime("%d-%m-%Y")

        aid = self.dataBase.control('create_id' , 'borrowHistory')
        borrow = Borrow(aid, user , book[0], book[1], start_date , due_date,'borrowed')
        isAdded = self.dataBase.control('add',borrow)
        if not isAdded:
            return
        self.auto.send_email_remainders('borrow',user , book[1] , start_date , due_date)



    def return_book(self):

        rows = self.dataBase.fitch('all_rows_return')
        print(rows)

        if not rows:
            print('There are no borrows history in dataBase!')
            return

        table = self.dataBase.fitch('all_table' , 'borrowed_books')
        print(tabulate(table , headers='keys'))


        book_identifier = input('Enter the id or title of the book: ')

        book = [row for row in rows if book_identifier == str(row[2]) or book_identifier == row[3]]

        returned_book = book

        if not book:
            print("We can't find the borrow!")
            return
        if len(book) > 1:
            print('Enter the name of the user that wants: ')
            user = input()
            returned_book = list(filter(lambda row:user == row[1] , book))
            if not returned_book:
                print('The user is not exist!')
                return

            if len(returned_book) > 1:
                table = self.dataBase.fitch('more than one', book_identifier)
                print(tabulate(table, headers='keys'))
                print(f'''There are {len(table)} different types of books matches the title you enter
chose the the book that you want by select an id: ''')

                while True:
                    user_book_id = input().strip()
                    if not user_book_id.isdigit():
                        print('The id must be only an <INTEGER> value! ')
                        continue

                    updated_book = [row for row in returned_book if user_book_id == str(row[2])]

                    if updated_book:
                        returned_book = updated_book
                        break
                    print('chose one of these ids only!')
                    continue
        try:
            self.dataBase.cursor.execute('UPDATE borrowHistory set status="returned" WHERE id=?',(returned_book[0][0],)  )
            self.dataBase.sql_connection.commit()
            self.dataBase.cursor.execute('UPDATE books set count=count+1 WHERE id=?', (returned_book[0][2],))
            self.dataBase.sql_connection.commit()
            print(f'"{returned_book[0][3]}" was returned to the Library')


        except Exception as error:
            print('DataBase error(return)', error)
            return
        self.auto.send_email_remainders('return', returned_book[0][1], returned_book[0][3])

    def display_control(self):
        table = self.dataBase.fitch('all_table', 'borrowHistory')
        if not table:
            print('Th+e dataBase is empty!')
            return
        print(tabulate(table, headers='keys'))
















