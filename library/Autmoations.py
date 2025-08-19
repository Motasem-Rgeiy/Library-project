from Library_main import Library
import csv , openpyxl
from Book import Book
from selenium import webdriver
from selenium.webdriver.common.by import By
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Automations(Library):

    def __init__(self,csv_file=None , excel_file=None):
        super().__init__()
        self.csv_file = csv_file
        self.excel_file = excel_file

    def user_input(self):
        while True:
            print('''1-Export
2-Import books
3-Web scraping
4-Exit'''
    )

            user = input()
            if user == '1':
                self.export_data()
            elif user == '2':
                self.import_books_data()
            elif user == '3':
                self.webScraping()
            elif user =='4':
                return user
            else:
                print('Invalid input!')

    def export_data(self):
            print('1-Export list of books\n2-Export list of borrow history')
            user = input()
            if user == '1':
                required_table = 'books'
            elif user == '2':
                required_table = 'borrowHistory'
            else:
                print('Invalid input')
                return


            all_rows = self.dataBase.fitch('all_rows' , required_table)
            if not all_rows:
                print('DataBase is empty!')
                return
            headers = self.dataBase.fitch('headers', required_table)
            all_rows.insert(0 , headers)


            #CSV
            try:
                with open(rf'{self.csv_file}' , 'w', newline='' ,encoding='utf-8') as file:
                    csvFile = csv.writer(file)
                    csvFile.writerows(all_rows)

                #Excel
                excel_file = openpyxl.Workbook()
                my_sheet = excel_file.create_sheet()
                my_sheet.title = required_table



                for row in range(0, len(all_rows)):
                    for col in range(0, len(all_rows[row])):
                        my_sheet.cell(column=col+1 , row=row+1).value = all_rows[row][col]


                excel_file.save(self.excel_file)
                print(f'"{required_table}" has exported to "{self.csv_file}" and "{self.excel_file}" successfully.')
            except csv.Error as error:
                print('Something wrong has been happened in CSV!' , error)
            except Exception as error:
                print('Something wrong has been happened!' , error)



    def import_books_data(self):

            def excel_import(file):
                excel_file = openpyxl.load_workbook(file)
                all_sheets = excel_file.sheetnames
                if 'books' not in all_sheets:
                    return
                my_sheet = excel_file['books']
                rows = list(my_sheet.values)[1:]
                return rows



            def csv_import(file):
                with open(file , 'r') as csvFile:
                    csv_reader = csv.reader(csvFile)
                    headers = self.dataBase.fitch('headers' , 'books')
                    csv_headers = [row for row in list(csv_reader)[0]]
                    try:
                        for i in range(len(headers)):
                            if headers[i] != csv_headers[i]:
                                return
                    except Exception as error:
                        print(error)
                        return

                    rows = [tuple(row) for row in list(csv_reader)[1:]]
                    return rows


            print('What file do you want to import from?\n1-CSV\n2-Excel')
            user = input().strip()
            if user == '1':
                 imported_data = csv_import(self.csv_file)
            elif user == '2':
                imported_data = excel_import(self.excel_file)
            else:
                print('Invalid input')
                return

            if not imported_data:
                print('There is no imported_data!')
                return




            all_dataBase_books = self.dataBase.fitch('all_rows', 'books')
            print(imported_data)


            if not all_dataBase_books:
                self.dataBase.cursor.executemany('INSERT INTO books VALUES(?,?,?,?,?,?,?)', (imported_data,) )
                self.dataBase.sql_connection.commit()
                return

            all_book_data = []

            for dataBase_row in all_dataBase_books:

                        dataBase_book = Book(dataBase_row[0] , dataBase_row[1] , dataBase_row[2] , dataBase_row[3], dataBase_row[4]
                        , dataBase_row[5] ,dataBase_row[6])
                        all_book_data.append(dataBase_book)

            for imported_data_row in imported_data:
                        imported_book = Book(imported_data_row[0], imported_data_row[1], imported_data_row[2] , imported_data_row[3]
                                    ,imported_data_row[4], imported_data_row[5] , imported_data_row[6])

                        if imported_book in all_book_data:
                            print(f'{imported_book.title} is already exist.')
                            continue

                        aid = self.dataBase.fitch('create_id', 'books')
                        self.dataBase.cursor.execute('INSERT INTO books VALUES(?,?,?,?,?,?,?)' ,(aid,imported_book.title,
                        imported_book.author, imported_book.year, imported_book.price, imported_book.classification, imported_book.count))
                        self.dataBase.sql_connection.commit()

    def webScraping(self):
        browser = webdriver.Chrome()
        browser.get('https://en.wikipedia.org/wiki/List_of_best-selling_books')
        table = browser.find_element(By.CSS_SELECTOR,
                                     '#mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child(13)')
        rows = table.find_elements(By.CSS_SELECTOR, 'tr')
        for row in rows:
            elements = row.find_elements(By.CSS_SELECTOR, 'td')
            ele_text = [element.text.strip() for element in elements]
            if not ele_text:
                continue
            aid = self.dataBase.fitch('create_id' ,'books')
            web_book = Book(aid , ele_text[0] , ele_text[1] , ele_text[3] , 0 ,ele_text[5])
            self.dataBase.control('add' , web_book)
        print('Data has been scraped from "https://en.wikipedia.org/wiki/List_of_best-selling_books" successfully.')
        browser.quit()




    def send_email_remainders(self, order, user, book_title, start_data=None, due_date=None):

            all_users = self.dataBase.fitch('all_rows', 'users')
            if not all_users:
                print('There is any register right now!')
                return
            sender_email = input('Enter the sender email: ')
            password = input('Enter the password: ')

            req_user = [user1 for user1 in all_users if user == user1[1]]
            if not req_user:
                print(f'The email is not sent to {user} because it has been deleted.')
                return

            receiver_email = req_user[0][2]


            if order == 'borrow':
                subject = "Borrow Confirmation"
                body = (f"Dear {user}, you have successfully borrowed '{book_title}' "
                        f"on {start_data}. Please return it by {due_date}. "
                        "Late returns may result in fees. Thank you, and happy reading!")

            elif order == 'return':
                subject = "Return Confirmation"
                body = (f"Dear {user}, we confirm that '{book_title}' was returned. "
                        "Thank you for returning it. Your account is now clear. "
                        "We look forward to seeing you again soon!")
            else:
                return

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain", "utf-8"))

            try:
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                print(f'The email was sent to {user} successfully.')
            except Exception as error:
                print('Sender email or password is not correct or there is another error!', error)
            finally:
                server.quit()


