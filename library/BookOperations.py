from Book import Book
import datetime
import re
from tabulate import tabulate
from Library_main import Library


class BookOperations(Library):
    def __init__(self):
        super().__init__()



    def user_input(self):
        while True:
            message = """--------------------------------
1-Add a book
2-Update a book
3-Search for a book
4-list all books
5-Delete a book
6-Reset
7-Exit
"""
            user = input(message).strip()
            if user == '1':
                self.add_book()
            elif user == '2':
                self.update_book()
            elif user == '3':
                self.search_book()
            elif user == '4':
                self.list_books()
            elif user == '5':
                self.delete_book()
            elif user == '6':
                self.dataBase.reset()
            elif user == '7':
                self.dataBase.close_db()
                return user

            else:
                print('Invalid input!')


    def input_processing(self , order , item):
        if order == 'title':
            if not item:
                print("You don't enter anything!!")
                return
            if item[0] in '.,!@#$%^&*()':
                 print('The first character must not be a symbol!')
                 return
            return item

        elif order == 'author':
            if not item:
                print("You don't enter anything!!")
                return
            if item[0].isdigit() or item[0] in '.,!@#$%^&*()':
                print('The first character must not be a digit or a symbol!')
                return
            return item

        elif order == 'year':
            if not item.isdigit():
                print('The year must be only <INTEGER> value!')
                return
            current_year = datetime.datetime.today().year
            if int(item) < 0 or int(item) > current_year:
                print('Invalid Year!')
                return
            return item
        elif order == 'price':
            check_price = re.search(r'^(\d+|\d+\.\d+)$',item)
            if not check_price:
                print('the price must be <FLOAT> value!')
                return
            return item
        elif order == 'count':
            try:
                item = int(item)
            except ValueError:
                print('The count must be only <INTEGER> value')
                return
            return item
        elif order == 'classification':
            return item

    def add_book(self):
        title = input('Enter a title: ')
        if not self.input_processing('title' , title):
            return

        author = input('Enter an author: ')
        if not self.input_processing('author', author):
            return

        year = input('Enter a year: ')
        if not self.input_processing('year' , year):
                return


        price = input('Enter the price: ')
        if not self.input_processing('price', price):
                return

        classification = input('Enter a classification: ')

        ida = self.dataBase.control('create_id','books')

        book = Book(ida,title , author , year ,float(price) , classification)
        self.dataBase.control('add' ,book)


    def update_book(self):
        book = self.title_id( 'update', 'books')
        if not book:
            return
        identifier,required_book = book[0] ,book[1]

        def ask_user():
            message = '''What thing do you want to update?
1-title 
2-author 
3-year 
4-price 
5-classification
6-count
'''
            number = input(message).strip()
            if number == '1':
                return 'title'
            elif number == '2':
                return 'author'
            elif number == '3':
                 return 'year'
            elif number == '4':
                return 'price'
            elif number == '5':
                return 'classification'
            elif number == '6':
                return 'count'
            else:
                print('Invalid input!')
                return 'Invalid input!'

        required_updated = ask_user()
        if required_updated == 'Invalid input!':
                return

        value = input('Enter a new value: ')
        check_new_value = self.input_processing(required_updated ,value)
        if not check_new_value and check_new_value != 0:
                    return
        return self.dataBase.update(required_updated, value, identifier, required_book)




    def delete_book(self):
        table = self.dataBase.control('all_table' ,'books')
        if not table:
            print('The dataBase is empty!')
            return

        print(tabulate(table , headers='keys'))
        print('You can delete a single book or range of books(maximum:3).\nEnter the id of the book you want to delete: ',end='')
        ids_range = []
        while True:
            deleted_id_book = input().strip()
            if not deleted_id_book:
                print('You did not enter anything!\nTry again: ',end='')
                continue
            ids_range = deleted_id_book.split(' ')
            ids_range = [b for b in ids_range if not b=='']
            if len(ids_range) > 3:
                print('You cannot delete more than 3 books in a single range!\nTry again: ',end='')
                continue
            if len(ids_range) == 1:
                if not deleted_id_book.isdigit():
                    print("The id must be only an <INTEGER> value\nTry again: ",end='')
                    continue
            elif all(value.isdigit() for value in ids_range):
                break
            else:
                print('All ids must be <INTEGER> values.\nTry again: ',end='')
                continue
            break

        filtered_deleted_ids = []
        non_deleted_ids = []

        all_ids = self.dataBase.control('ids')

        for aid in ids_range:
            if aid in all_ids and aid not in filtered_deleted_ids:
                filtered_deleted_ids.append(aid)
                continue
            elif aid not in filtered_deleted_ids and aid not in non_deleted_ids:
                non_deleted_ids.append(aid)
        print(filtered_deleted_ids)
        if not filtered_deleted_ids:
            print('The ids do not match any existing id!')
            return
        if non_deleted_ids:
            print('The following IDs are not exist: ')
            for non_id in non_deleted_ids:
                print(non_id)
        return self.dataBase.control('delete book', filtered_deleted_ids)



    def search_book(self):
        rows = self.dataBase.fitch('all_rows','books')
        if not rows:
            print('The dataBase is empty!')
            return
        print('You can search by a "Title" or an "Author" or a "Classification": ',end='')
        while True:
            searched_book = input().strip()
            if not searched_book:
                print('You do not enter anything!\nTry again: ',end='')
                continue
            break
        result =  self.dataBase.fitch('search by', searched_book)
        if not result:
            print('Sorry, There is no result!')
            return
        print(tabulate(result, headers='keys'))

    def list_books(self):
        table = self.dataBase.fitch('all_table' , 'books')
        if not table:
            print('DataBase is empty!')
            return
        print(tabulate(table , headers='keys'))

    def title_id(self, order, rows):
            book_rows = self.dataBase.fitch('all_rows', rows)

            if not book_rows:
                print('DataBase is empty!')
                return

            table = self.dataBase.fitch('all_table', rows)
            print(tabulate(table, headers='keys'))
            user = input('Enter the title or id of the book: ')

            borrowed_book = []
            if order == 'update':
                for row in book_rows:
                    if user == str(row[0]):
                        borrowed_book.append(row)
                        identifier = 'id'
                        break
                    if user == row[1]:
                        borrowed_book.append(row)
                        identifier = 'title'
            elif order == 'borrow':
                borrowed_book = [row for row in book_rows if user == str(row[0]) or user == row[1]]

            updated_book = borrowed_book
            if len(borrowed_book) > 1:
                identifier = 'id'
                table = self.dataBase.fitch('more than one', user)
                print(tabulate(table, headers='keys'))
                print(f'''There are {len(table)} different types of books matches the title you enter
chose the the book that you want by select an id: ''')
                while True:
                    user = input().strip()
                    if not user.isdigit():
                        print('The id must be only an <INTEGER> value! ')
                        continue

                    updated_book = [row for row in borrowed_book if user == str(row[0])]

                    if updated_book:
                        break
                    print('chose one of these ids only!')
                    continue

            if not updated_book:
                print('The book is not exist!')
                return

            if order == 'update':
                return identifier, user
            elif order == 'borrow':
                if updated_book[0][-1] < 1:
                    print("The book's count has finished!")
                    return
                return updated_book[0]








