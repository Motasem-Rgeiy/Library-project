class Borrow:
    def __init__(self, id, user, book_id,  book_title,start_date, due_date,status):
        self.id = id
        self.user = user
        self.book_id= book_id
        self.book_title = book_title
        self.start_date = start_date
        self.due_date = due_date
        self.status = status
    def __str__(self):
        print(f'{self.id}, {self.user}, {self.book_id}, {self.book_title}, {self.start_date}, {self.due_date}, {self.status}')

    def __eq__(self, other):
        return self.book_id == other.book_id and self.user == other.user and other.status == 'borrowed'