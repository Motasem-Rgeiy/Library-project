import sqlite3
from Book import Book
from User import User
from Borrow import Borrow

class DataBaseManagement:
    def __init__(self, file_name):
            self.sql_connection = sqlite3.connect(file_name)
            self.cursor = self.sql_connection.cursor()
            self.create()

    def control(self , order , task=None):

        if order == 'create_id':
            return self.fitch('create_id',task)

        elif order == 'add':
            if isinstance(task, User):
                all_details1=self.fitch('all_rows','users')
            elif isinstance(task, Book):
                all_details1 = self.fitch('all_rows', 'books')
            elif isinstance(task, Borrow):
                all_details1 = self.fitch('all_rows', 'borrowHistory')
            else:
                print('Control function Error')
                return
            return self.add(task  , all_details1)

        elif order == 'all_table':
                return self.fitch('all_table' , task)

        elif order == 'more than one':
            return self.fitch('more than one' , task)

        elif order == 'titles' or order == 'ids':
            return self.fitch(order)

        elif order == 'delete book':
            return self.delete(task)



    def create(self):
        sql_creation = """CREATE TABLE if not exists books(
id INTEGER,
title VARCHAR(30),
author TEXT,
year VARCHAR(20),
price FLOAT,
classification TEXT,
count INTEGER)"""
        self.cursor.execute(sql_creation)
        sql_creation = """CREATE TABLE if not exists users(
id INTEGER,
name TEXT,
email TEXT,
phone TEXT)"""
        self.cursor.execute(sql_creation)

        sql_creation = """CREATE TABLE if not exists borrowHistory(
id INTEGER,
user TEXT,
book_id INTEGER,
book_title TEXT,
first_data TEXT,
due_data TEXT,
status TEXT)"""
        self.cursor.execute(sql_creation)
        self.sql_connection.commit()



    def add(self,added_element, all_details):
        try:
            if isinstance(added_element, Book):
                new_book = added_element
                for book_details in all_details:
                    old_book = Book(book_details[0] , book_details[1] , book_details[2] , book_details[3], book_details[4],
                                    book_details[5], book_details[6])

                    if new_book == old_book:
                        old_book.count+=1
                        self.cursor.execute('UPDATE books set count=? WHERE id=?' ,(old_book.count,old_book.id))
                        self.sql_connection.commit()
                        print(f'"{new_book.title}" has added successfully.')
                        return

                self.cursor.execute('INSERT INTO books VALUES(?,?,?,?,?,?,?)',
                                   (new_book.id,new_book.title,new_book.author,new_book.year,new_book.price,new_book.classification,new_book.count))
                self.sql_connection.commit()
                print(f'{new_book.title} has added successfully.')

            elif isinstance(added_element, User):
                new_user = added_element
                self.cursor.execute('INSERT INTO users VALUES(?,?,?,?)', (new_user.id,new_user.name,new_user.email,new_user.phone_number))
                self.sql_connection.commit()
                print(f'"{new_user.name}" has been added successfully.')
                return

            elif isinstance(added_element ,Borrow):
                new_loan = added_element
                for details in all_details:
                    old_loan = Borrow(details[0], details[1], details[2], details[3], details[4], details[5], details[6])
                    if new_loan == old_loan:
                        print('The user can not borrow the same book twice!')
                        return


                self.cursor.execute('INSERT INTO borrowHistory VALUES (?,?,?,?,?,?,?)', (
                new_loan.id, new_loan.user, new_loan.book_id, new_loan.book_title, new_loan.start_date, new_loan.due_date, new_loan.status))
                self.sql_connection.commit()

                self.cursor.execute('UPDATE books set count =count-1 WHERE id=?',(new_loan.book_id,))
                self.sql_connection.commit()

                print(f'"{new_loan.user}" has borrowed "{new_loan.book_title}" until "{new_loan.due_date}"')
                return True

        except sqlite3.Error as error:
            print('DataBase Error (add)' ,error)


    def update(self, required_updated, value, identifier, required_book):
        try:
            allowed_columns = ["title", "author", "year", "price", "classification", "count"]
            if required_updated not in allowed_columns or identifier not in ["id", "title"]: #To make more security
                print("Invalid update parameters!")
                return
            self.cursor.execute(f'UPDATE books set {required_updated}=? WHERE {identifier}=?', (value , required_book))
            self.cursor.execute(f'SELECT title FROM books WHERE {identifier}=?', (required_book,))
            updated_book = self.cursor.fetchone()[0]

            self.sql_connection.commit()
            print(f'The "{required_updated}" of "{updated_book}" has updated to "{value}" successfully.')

        except sqlite3.Error as error:
            print('DataBase Error (update)', error)


    def delete(self, deleted_book_ids):
        try:

            for ida in deleted_book_ids:
                self.cursor.execute('DELETE FROM books WHERE id=?', (ida,))
                self.sql_connection.commit()

        except sqlite3.Error as error:
            print('DataBase Error (delete)', error)


    def fitch(self , task,value=None):
        try:
            if task == 'create_id': #1
                        last_id = 1
                        self.cursor.execute(f'SELECT COUNT(*) FROM {value}')
                        count = self.cursor.fetchone()[0]
                        if count == 0:
                            return last_id
                        self.cursor.execute(f'SELECT id FROM {value}')
                        last_id = self.cursor.fetchall()[-1][0]
                        return last_id+1

            elif task == 'all_rows': #2
                self.cursor.execute(f'SELECT * FROM {value}')
                all_rows = self.cursor.fetchall()
                return all_rows



            elif task == 'all_table' or task == 'more than one': #3

                if task == 'all_table':

                    if value == 'borrowed_books':
                        self.cursor.execute(f'SELECT id,user,book_id,book_title,first_data,due_data FROM borrowHistory WHERE status="borrowed"')
                    else:
                        self.cursor.execute(f'SELECT * FROM {value}')

                else:
                        self.cursor.execute('SELECT * FROM books WHERE title=?' , (value,))

                rows = self.cursor.fetchall()
                headers = [head[0] for head in self.cursor.description]
                values_display = []
                for row in rows:
                    values_display.append(dict(zip(headers, row)))
                return  values_display


            elif task == 'search by': #4
                self.cursor.execute('SELECT * FROM books')
                rows = self.cursor.fetchall()

                if not rows:
                    return

                headers = [head[0] for head in self.cursor.description]
                values_display = []
                for row in rows:
                    if value in row:
                        values_display.append(dict(zip(headers, row)))
                return values_display

            elif task =='all_rows_return':
                self.cursor.execute('SELECT * FROM borrowHistory WHERE status="borrowed"')
                return self.cursor.fetchall()

            elif task == 'headers':
                self.cursor.execute(f'SELECT * FROM {value}')
                headers = [head[0] for head in self.cursor.description]
                return headers

            elif task == 'ids':
                self.cursor.execute('SELECT id FROM books')
                all_ids = [str(id[0]) for id in self.cursor.fetchall()]
                return  all_ids

        except sqlite3.Error as error:
            print('DataBase error (fitch)' , error)


    def reset(self):
        try:
            dec = input('Are you sure?(y)').strip()
            if dec != 'y':
                return

            self.cursor.execute('DELETE FROM books')
            self.sql_connection.commit()
            print('Reset process has been done!')
        except sqlite3.Error as error:
            print('DataBase Error (reset)', error)


    def close_db(self):
        try:
            print('The program has closed.')
            self.sql_connection.close()
        except sqlite3.Error as error:
            print('DataBase Error (close)', error)

















