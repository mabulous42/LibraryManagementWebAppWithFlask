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
    library.get_user(user_id)    

# function to edit or modify user name
def edit_user(library, user_id, new_name):
    library.edit_user(user_id, new_name)

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
            users = [user.to_dict() for user in library.users.values()]
            json.dump(users, user_file, indent=4)
        print("User data saved.")
    except Exception as e:
        print(f"Failed to save users: {e}")


# Save books to books.json
def save_books(library):
    try:
        with open('books.json', 'w') as book_file:
            books = [book.to_dict() for book in library.books.values()]
            json.dump(books, book_file, indent=4)
        print("Book data saved.")
    except Exception as e:
        print(f"Failed to save books: {e}")


# Load users from users.json
def load_users(library):
    try:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)
            for user_data in users:
                user = User.from_dict(user_data)
                library.users[user.user_id] = user
        print("User data loaded.")
        return library.users
    except FileNotFoundError:
        print("No user data found.")


# Load books from books.json
def load_books(library):
    try:
        with open('books.json', 'r') as book_file:
            books = json.load(book_file)
            for book_data in books:
                book = Book.from_dict(book_data)
                library.books[book.isbn] = book
        print("Book data loaded.")
        return library.books
    except FileNotFoundError:
        print("No book data found.")


