from datetime import datetime, timedelta
from flask_login import UserMixin



# defining classes
class Book:
    # initialising the book attributes (title, author, isbn, available_copies)
    def __init__(self, title, author, isbn, available_copies = 0):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available_copies = available_copies
        self.added_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        

    # string method to display the book information
    def __str__(self):
        return f"'{self.title}' by {self.author} | ISBN: {self.isbn} | Copies: {self.available_copies}"

    # function to convert book object into dictionary data when loading from json file
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available_copies": self.available_copies,
            "added_at": self.added_at
        }

    # function to convert book dictionary into object when saving into json file
    @staticmethod
    def from_dict(data):
        book = Book(data["title"], data["author"], data["isbn"], data["available_copies"])
        book.added_at = data['added_at']
        return book

class User(UserMixin):
    # initialising the User attributes (name, user_id, borrowed_books_ISBN)
    def __init__(self, name, user_id, email, password):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.password = password
        self.borrowed_books = []
        self.registered_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def get_id(self):
        return self.user_id
    
    @property
    def id(self):
        return self.user_id 

    # method to create a list of borrowed book(s) using the book isbn
    def borrow_book(self, isbn):
        borrowed_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
        # Default: 2 weeks from borrow date
        borrow_dt = datetime.strptime(borrowed_date, "%d-%m-%Y %H:%M:%S")
        return_dt = borrow_dt + timedelta(days=14)
        return_date = return_dt.strftime("%d-%m-%Y %H:%M:%S")
    
        borrowed_book_record = {
            'isbn': isbn,
            'borrowed_date': borrowed_date,
            'return_date': return_date,
            'returned': False  # Track if book has been returned
        }
        
        self.borrowed_books.append(borrowed_book_record)

    # method to remove a book from the list of borrowed books using the book isbn
    def return_book(self, isbn):
        """Mark a book as returned"""
        for book in self.borrowed_books:
            if book['isbn'] == isbn and not book['returned']:
                book['returned'] = True
                book['actual_return_date'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                return True
        return False

    def get_active_borrowed_books(self):
        """Get only books that haven't been returned"""
        return [book for book in self.borrowed_books if not book['returned']]

    # string method to display a User's information 
    def __str__(self):
        return f"Name: {self.name} | ID: {self.user_id} | {self.email} | Borrowed: {self.borrowed_books}"

    # function to convert user object into dictionary data when loading from json file
    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "email": self.email,
            "password": self.password.decode('utf-8') if hasattr(self.password, 'decode') else self.password,
            "borrowed_books": self.borrowed_books,
            "registered_at": self.registered_at
        }

    # function to convert user dictionary into object when saving into json file
    @staticmethod
    def from_dict(data):
        user = User(data["name"], data["user_id"], data["email"], data["password"])
        user.borrowed_books = data["borrowed_books"]
        user.registered_at = data["registered_at"]
        return user
    
class AdminUser(UserMixin):
    def __init__(self):
        self.id = 'admin'
        self.email = 'admin@mustyl-library.com'
        self.username = 'Admin'
        self.password = 'admin101'
        self.is_admin = True
    
    def get_id(self):
        return self.id

        
class Library:
    # initialising the library attributes (books and users)
    def __init__(self):
        self.books = {} # (dictionary of isbn: Book)
        self.users = {} # (dictionary of user_id: User)
        
    # library book methods
    # methods to add book using their isbn as the key value into the dictionary of books
    def add_book(self, new_book):
        # condition to check if a different book with the same isbn is not present in the list
        if new_book.isbn in self.books:
            print('Ooooops! Book with this ISBN already exist')
        else:
            self.books[new_book.isbn] = new_book
            print(f"Book with ISBN: {new_book.isbn} has been addedd successfully.")
            print(new_book)
        
    # methods to remove book using their isbn from the dictionary of books
    def remove_book(self, isbn):
        if isbn in self.books:
            self.books.pop(isbn)
            print(f"Book with ISBN: {isbn} has been removed successfully.")
        else:
            print(f"Book with ISBN: {isbn} was not found in the book collection")

    # method to search for a book from the dictionary of books using the book title
    def search_books(self, title):
        result = [] # just incase there are more than one books matching the search
        for book in self.books.values():
            if title.lower() in book.title.lower():
                result.append(book) # this saves the matching book(s)
        return result # this returned all the matching books
                
    # library user methods
    # methods to register a new library user
    def register_user(self, new_user):
        if new_user.user_id in self.users:
            print(f"User {new_user.id} already exist")
        else:
            self.users[new_user.user_id] = new_user
            print(f"Name: {new_user.name} | user_id: {new_user.user_id} has been added successfully.")

    def get_user_by_id (self, user_id):
        if user_id in self.users:
            user = self.users[user_id]
            return user
        else:
            return "User not found"
        
    def get_book_by_isbn(self, isbn):
        if isbn in self.books:
            book = self.books[isbn]
            return book
        else:
            return "Book not found"
        
    def get_user_email(self, email):
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def edit_user(self, user_id, new_name, new_email):
        if user_id in self.users:
            user = self.users[user_id]
            user.name = new_name
            user.email = new_email

    def edit_book(self, isbn, new_isbn, new_title, new_author, update_available_copies):
        if isbn in self.books:
            book = self.books[isbn]
            book.isbn = new_isbn
            book.title = new_title
            book.author = new_author
            book.available_copies = update_available_copies

    # methods to delete user using their user_id from the dictionary of users
    def delete_user(self, user_id):
        if user_id in self.users:
            user = self.users[user_id]
            # checking if the user has any borrowed book(s), the user cannot be deleted
            if user.borrowed_books:
                print(f"\nCannot delete user {user_id}! User still has one or more borrowed books")
                print(f"Borrowed book: {user.borrowed_books}")
                return
                
            # if user does not have any borrowed book(s), then the user can be deleted    
            self.users.pop(user_id)
            print(f"User with user_id: {user_id} has been removed successfully.")
        else:
            print(f"User with user_id: {user_id} does not exist")

     # method to search for a user from the dictionary of users using the user's name
    def search_users(self, name):
        result = [] # just incase there are more than one user matching the search
        for user in self.users.values():
            if name.lower() in user.name.lower():
                result.append(user) # this saves the matching user(s)
        return result # this returned all the matching users

    # method to borrow book from the library
    def borrow_book(self, user_id, isbn):
        # checking for two conditions which needs to be met; 
        # the user_id is used to check if the user exist and the book isbn to check if the book exist in the User and Book collection respectively
        if user_id in self.users and isbn in self.books:
            user = self.users[user_id] # getting the user details into user
            if len(user.borrowed_books) > 5:
                print(f"This user {user_id} have reached the maximum number of books that he/she can borrow (5)")
            elif any(b['isbn'] == isbn for b in user.borrowed_books):
                print("You cannot borrow the same book that you have already borrowed")
            else:
                book = self.books[isbn] # getting the book details into book
                if book.available_copies > 0: # checking if there is at least a copy or more copies of book available to borrow
                    book.available_copies -= 1
                    user.borrow_book(isbn)
                    print(f'{user.name}, your request to borrow book title: {book.title} is successful')
                else:
                    print('No copies available')
        else:
            print(f"User {user_id} or book not found")

    # method to return borrowed book back to the library
    def return_book(self, user_id, isbn):
        # checking for two conditions which needs to be met; 
        # the user_id is used to check if the user exist and the book isbn to check if the book exist in the User and Book collection respectively
        if user_id in self.users and isbn in self.books:
            user = self.users[user_id] # getting the user details into user
            book = self.books[isbn] # getting the book details into book
            if isbn in user.borrowed_books:
                user.return_book(isbn)
                book.available_copies += 1
                print(f'{user.name} returned {book.title}')
            else:
                print(f"The book with {isbn} is not among {user.name} borrowed book ")
           

    # additional function to view all books in the library
    def view_all_books(self):
        # if there is no book in the library
        if not self.books:
            print("No books available in the library.")
        else:
            print("\nAll Books in the Library:")
            for book in self.books.values():
                return book

    # additional function to view all users in the library
    def view_all_users(self):
        # if there is no book in the library
        if not self.users:
            print("Library user's list is currently empty.")
        else:
            print("\nAll users in the Library:")
            for user in self.users.values():
                print(user)

class EBook:
    def __init__(self, title, author, isbn, format, file_path):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.format = format
        self.file_path = file_path
        self.added_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"EBook: '{self.title}' by {self.author} | Format: {self.format} | ISBN: {self.isbn}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "format": self.format,
            "file_path": self.file_path,
            "added_at": self.added_at
        }

    @staticmethod
    def from_dict(data):
        ebook = EBook(
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            format=data["format"],
            file_path=data["file_path"]
        )
        ebook.added_at = data.get("added_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return ebook

                
class digitalLibrary(Library):
    def __init__(self):
        super().__init__() # setting up the inital Library attributes; self.books = {} and self.users={}
        self.ebooks = {} # adding new attribute to the digital library
        
    # digitalLibrary methods
    # additional methods to add ebook to the diitalLibrary
    def add_ebook(self, ebook):
        if ebook.isbn in self.ebooks:
            print(f"EBook with ISBN {ebook.isbn} already exists.")
        else:
            self.ebooks[ebook.isbn] = ebook
            print(f"EBook '{ebook.title}' added successfully.")

    def read_ebook(self, isbn):
        # Checks if the given `isbn` exists in the `ebooks` dictionary
        if isbn in self.ebooks:
            print(f"Opening eBook file at: {self.ebooks[isbn]}")
        else:
            print("eBook not available.")

    # function to convert book object into dictionary data when loading from json file
    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "format": self.format,
            "added_at": self.added_at,
            "file_path": self.file_path
        }

    # function to convert book dictionary into object when saving into json file
    @staticmethod
    def from_dict(data):
        ebook = Book(data["title"], data["author"], data["isbn"])
        ebook.format = data["format"]
        ebook.added_at = data['added_at']
        ebook.file_path = data["file_path"]

        return ebook 
        