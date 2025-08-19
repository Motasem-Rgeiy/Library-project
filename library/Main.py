import os
import psutil
from BookOperations import BookOperations
from UserOperations import UserOperations
from Autmoations import Automations
from Borrow_Return_Management import BorrowReturn
from DataBaseManagement import DataBaseManagement
from pathlib import Path

def main():
    csvFile = Path.home() / Path('Desktop','Library', 'library',  'files' , 'data_c.csv')
    excelFile = Path.home() / Path('Desktop' ,'Library', 'library' , 'files' , 'data_e.xlsx')
    books = BookOperations()
    users = UserOperations()
    automation_process = Automations(csvFile, excelFile)
    borrow_return_process = BorrowReturn()
    dataBase = DataBaseManagement('Library.db')

    message = '''1-Books Management
2-Users Management
3-Borrow&Return Management
4-Automations
5-Close'''
    while True:
        print(message)
        process = input("Enter your choice: ")

        if process == '1':
            order = books.user_input()
            print(order)
            if order == '7':
                main()

        elif process == '2':
            order = users.user_input()
            if order == '3':
                main()

        elif process == '3':
            order = borrow_return_process.user_input()
            if order == '4':
                main()

        elif process == '4':
            order = automation_process.user_input()
            if order == '4':
                main()

        elif process == '5':
            dataBase.close_db()
            process_info = psutil.Process(os.getpid())
            print(f"Final Memory used: {process_info.memory_info().rss / 1024**2:.2f} MB")
            break
        else:
            print('Invalid input!')
            continue
        
        return

if __name__ == '__main__':
    main()