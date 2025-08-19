class Book:
    def __init__(self,id, title, author, year, price, classification,count=1):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.price = price
        self.classification = classification
        self.count = count

    def __str__(self):
        return f'{self.id},{self.title}, {self.author}, {self.year}, {self.price}, {self.classification}, {self.count}'

    def __eq__(self, other):
        if isinstance(other , Book):
            return self.title == other.title and self.author == other.author and self.year == other.year and  self.price == other.price and self.classification==other.classification
        return NotImplemented

    def __iter__(self):
        """Allows the object to be unpacked or converted to tuple."""
        yield self.id
        yield self.title
        yield self.author
        yield self.year
        yield  self.price
        yield self.classification
        yield self.count












