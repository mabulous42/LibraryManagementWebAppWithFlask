# functions
import json
from models import Book, Library, User, digitalLibrary

# function to add a book to the library
def add_book(library, book):
    library.add_book(book)

# function to register a new user
def register_user(library, user):
    library.register_user(user)

# function to get a user by id
def get_user_by_id(library, user_id):
    return library.get_user_by_id(user_id)    

# function to edit or modify user name
def edit_user(library, user_id, new_name, new_email):
    library.edit_user(user_id, new_name, new_email)

# function to borrow a book from the library
def borrow_book(library, user_id, isbn):
    library.borrow_book(user_id, isbn)

#function to return a borrowed book back to the library
def return_book(library, user_id, isbn):
    library.return_book(user_id, isbn)

# function to search for books
def search_books(library, title):
    return library.search_books(title)

# function to search for a library users
def search_users(library, name):
    return library.search_users(name)

# function to delete a user
def delete_user(library, user_id):
    library.delete_user(user_id)

# Save users to users.json
def save_users(library):
    try:
        with open('users.json', 'w') as user_file:
            users_dict = {}
            for user_id, user in library.users.items():
                users_dict[user_id] = user.to_dict()
            json.dump(users_dict, user_file, indent=4)
        print("User data saved.")
    except Exception as e:
        print(f"Failed to save users: {e}")


# Save books to books.json
def save_books(library):
    try:
        with open('books.json', 'w') as book_file:
            books_dict = {}
            for isbn, book in library.books.items():
                books_dict[isbn] = book.to_dict()
            json.dump(books_dict, book_file, indent=4)
        print("Book data saved.")
    except Exception as e:
        print(f"Failed to save books: {e}")


# Load users from users.json
def load_users(library):
    try:
        with open('users.json', 'r') as user_file:
            users_dict = json.load(user_file)
            
            # Clear existing users
            library.users = {}
            
            # Load from dictionary structure
            for user_id, user_data in users_dict.items():
                user = User.from_dict(user_data)
                library.users[user_id] = user
                
        print("User data loaded.")
        return library.users
    except FileNotFoundError:
        print("No user data found.")
        return {}
    except Exception as e:
        print(f"Failed to load users: {e}")
        return {}


# Load books from books.json
def load_books(library):
    try:
        with open('books.json', 'r') as book_file:
            books_dict = json.load(book_file)
            
            # Clear existing users
            library.books = {}
            
            # Load from dictionary structure
            for isbn, book_data in books_dict.items():
                book = Book.from_dict(book_data)
                library.books[isbn] = book
                
        print("Book data loaded.")
        return library.books
    except FileNotFoundError:
        print("No book data found.")
        return {}
    except Exception as e:
        print(f"Failed to load books: {e}")
        return {}
    
# Save books to books.json
def save_ebooks(digitalLibrary):
    try:
        with open('books.json', 'w') as book_file:
            books_dict = {}
            for isbn, book in digitalLibrary.books.items():
                books_dict[isbn] = book.to_dict()
            json.dump(books_dict, book_file, indent=4)
        print("Book data saved.")
    except Exception as e:
        print(f"Failed to save books: {e}")

# Load books from books.json
def load_ebooks(digitalLibrary):
    try:
        with open('books.json', 'r') as book_file:
            books_dict = json.load(book_file)
            
            # Clear existing users
            digitalLibrary.books = {}
            
            # Load from dictionary structure
            for isbn, book_data in books_dict.items():
                book = Book.from_dict(book_data)
                digitalLibrary.books[isbn] = book
                
        print("Book data loaded.")
        return digitalLibrary.books
    except FileNotFoundError:
        print("No book data found.")
        return {}
    except Exception as e:
        print(f"Failed to load books: {e}")
        return {}


