import json, os
from numpy import random
from flask import Flask, render_template, url_for, request, redirect, flash, abort
from forms import SignupForm, LoginForm, AddBookForm, AddeBookForm, UpdateUserForm, UpdateBookForm, SearchUserForm, SearchBookForm, BorrowBookForm
from flask_bcrypt import Bcrypt
from models import User, Book, Library, AdminUser, digitalLibrary
from helpers import register_user, load_books, load_users, save_books, save_users, add_book, load_ebooks, delete_user, get_user_by_id, edit_user, remove_book, get_book_by_isbn, edit_book, search_users, search_books, borrow_book, time_ago, return_book
from datetime import datetime
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' #This will make flashing messages work perfectly and support Flask extensions like Flask-WTF.


bcrypt = Bcrypt(app)
library = Library()
dglibrary = digitalLibrary()
load_users(library)
load_books(library)
load_ebooks(digitalLibrary)


admin_user = AdminUser()

# Hard-coded admin credentials
ADMIN_EMAIL = admin_user.email
ADMIN_PASSWORD = admin_user.password


# flask-login parameters
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader # this keeps track of the logged in user (current_user)
def load_user(user_id):
    if user_id == 'admin':      # checks if the user_id is admin then load user to be admin instead of the normal library users
        return AdminUser()
    
    user = library.get_user_by_id(user_id)  # this is where the actual library users is been loaded after the id is been fetched successfully
    return user



# admin decorator to make sure any user cannot have access to the admin features
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # Check if current user is admin
        if not isinstance(current_user, AdminUser):
            abort(403)  # Forbidden
        
        return f(*args, **kwargs)
    return decorated_function



@app.route("/")
def home():
    return render_template("index.html")
    



@app.route("/signup", methods=['GET','POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        num = random.randint(0, 9999)
        id = "{:03}".format(num)
        user_id = 'LU0' + id
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        firstName = form.firstName.data
        lastName = form.lastName.data
        name = firstName + " " + lastName

        new_user = User(name, user_id, form.email.data, hashed_password) #called the class User() constructor to create a new library user
        register_user(library, new_user) #called the register function from the helpers.py to register a new user

        save_users(library) #saving the new user into json storage

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    flash('User Already Exist', 'fail')

    return render_template("signup.html", form=form)





@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = library.get_user_email(form.email.data)
        admin_email = form.email.data
        admin_password = form.password.data

        if admin_email == ADMIN_EMAIL and admin_password == ADMIN_PASSWORD:
            login_user(admin_user)
            flash('Admin login successful!', 'success')
            return redirect(url_for('adminDashboard'))

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('userDashboard'))
        
    
    return render_template("login.html", form=form)

# User Features
@app.route('/userDashboard', methods=['GET', 'POST'])
@login_required
def userDashboard():
    library_books = load_books(library)
    library_books = [book.to_dict() for book in library_books.values()]

    borrowed_books_data = []

    user = current_user
    print(f"User authenticated: {user.is_authenticated}")
    print(f"User ID: {user.id}")
    print(f"User object: {user}")

    full_name = user.name.strip()
    name_parts = full_name.split()

    user_first_name = name_parts[0]
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""  # handle middle names or no last name

    for borrowed in user.borrowed_books:
        for book in library_books:
            if borrowed['isbn'] == book['isbn']:
                data = {
                    'title': book['title'],
                    'isbn': borrowed['isbn'],
                    'borrowed_date': borrowed['borrowed_date'],
                    'return_date': borrowed['return_date'][:10],
                    'return_status': borrowed['returned']
                }
                borrowed_books_data.append(data)

    # # Sorting by the datetime (most recent first)
    borrowed_books_data.sort(
        key=lambda book: datetime.strptime(book['borrowed_date'], '%d-%m-%Y %H:%M:%S'), 
        reverse=True
    )
        
    # Now converting to "time ago" format
    for book in borrowed_books_data:
        book['borrowed_date'] = time_ago(book['borrowed_date'])

    # borrowed_books_data.sort(key=lambda book: book['borrowed_date'])
        
    print ('borrowed_book: ', borrowed_books_data)

    return render_template('user/userDashboard.html', 
                           user = user, 
                           user_first_name = user_first_name, 
                           active_page = 'userDashboard',
                           borrowed_books_data = borrowed_books_data
                           )


@app.route('/user/borrowed_books', methods=['GET', 'POST'])
@login_required
def user_borrowed_books():
    user = current_user
    library_books = load_books(library)
    library_books = [book.to_dict() for book in library_books.values()]

    borrowed_books_data = []

    user_name = user.name.split()
    user_first_name = user_name[0]

    for borrowed in user.borrowed_books:
        for book in library_books:
            if borrowed['isbn'] == book['isbn']:
                data = {
                    'title': book['title'],
                    'isbn': borrowed['isbn'],
                    'borrowed_date': borrowed['borrowed_date'],
                    'return_date': borrowed['return_date'][:10],
                    'return_status': borrowed['returned']
                }
                borrowed_books_data.append(data)
            

    # # Sorting by the datetime (most recent first)
    borrowed_books_data.sort(
        key=lambda book: datetime.strptime(book['borrowed_date'], '%d-%m-%Y %H:%M:%S'), 
        reverse=True
    )
        
    # Now converting to "time ago" format
    for book in borrowed_books_data:
        book['borrowed_date'] = time_ago(book['borrowed_date'])

    # borrowed_books_data.sort(key=lambda book: book['borrowed_date'])
        
    print ('borrowed_book: ', borrowed_books_data)

    return render_template('user/view_borrowed_books.html', 
                           user = user, 
                           user_first_name = user_first_name, 
                           active_page = 'view_borrowed_books',
                           borrowed_books_data = borrowed_books_data
                           )

@app.route('/user/library_books', methods=['GET', 'POST'])
@login_required
def library_books():
    user = current_user
    form = BorrowBookForm()

    user_name = user.name.split()
    user_first_name = user_name[0]

    books = []

    if form.validate_on_submit():
        isbn = form.isbn.data

        try:
            borrow_book(library, user.user_id, isbn)
            save_books(library)
            save_users(library)
            flash("Book borrowed successfully!", "success")
        except Exception as e:
            flash(f"Error borrowing book: {str(e)}", "error")

        return redirect(url_for("library_books"))

    return render_template("user/library_books.html", 
                           active_page = 'library_books', 
                           user = user,
                           form = form,
                           books = books,
                           user_first_name = user_first_name
                           )


@app.route('/user/borrow_books/<user_id>/<isbn>', methods=['GET', 'POST'])
@login_required
def borrow_books(user_id, isbn):
    try:
        borrow_book(library, user_id, isbn)
        save_books(library)
        save_users(library)
        flash("Book borrowed successfully!", "success")
    except Exception as e:
        flash(f"Error borrowing book: {str(e)}", "error")

    return redirect(url_for("library_books"))

@app.route('/user/return_book/<user_id>/<isbn>')
@login_required
def user_return_book(user_id, isbn):

    print(user_id, isbn)


    return_book(library, user_id, isbn)
    save_books(library)
    save_users(library)

    return redirect(url_for('user_borrowed_books'))

@app.route('/user/search_books', methods=['GET', 'POST'])
@login_required
def user_search_books():
    user = current_user
    form = SearchBookForm()
    library_books = load_books(library)
    library_books = [book.to_dict() for book in library_books.values()]

    library_books.sort(key=lambda book: book['title'])

    search_made = False

    user_name = user.name.split()
    user_first_name = user_name[0]

    searched_books = []

    if form.validate_on_submit():
        title = form.title.data
        searched_books = search_books(library, title)
        search_made = True

        for book in searched_books:
            print(book)

        return render_template('user/user_search_book.html', 
                               active_page = 'user_search_books',  
                               form=form, 
                               searched_books = searched_books,
                               user = user,
                               user_first_name = user_first_name,
                               library_books = library_books,
                               search_made = search_made
                               )

    print(search_made) 

    return render_template("user/user_search_book.html", 
                           active_page = 'user_search_books', 
                           user = user,
                           form = form,
                           searched_books = searched_books,
                           user_first_name = user_first_name,
                           library_books = library_books,
                           search_made = search_made
                           )

# Admin Features
@app.route('/adminDashboard', methods=['GET', 'POST'])
@login_required
def adminDashboard():
    admin_user = current_user
    print(f"User authenticated: {admin_user.is_authenticated}")
    print(f"User ID: {admin_user.id}")
    print(f"User object: {admin_user}")

    library_users = load_users(library)
    library_books = load_books(library)

    library_users = [user.to_dict() for user in library_users.values()]
    library_books = [book.to_dict() for book in library_books.values()]

    borrowed_books_data = []

    for user in library_users:
        for borrowed in user['borrowed_books']:
            for book in library_books:
                if borrowed['isbn'] == book['isbn']:
                    data = {
                        'name': user['name'],
                        'title': book['title'],
                        'isbn': borrowed['isbn'],
                        'user_id': user['user_id'],
                        'borrowed_date': borrowed['borrowed_date'],
                        'return_date': borrowed['return_date'][:10],
                        'return_status': borrowed['returned']
                    }
                    borrowed_books_data.append(data)

    # # Sorting by the datetime (most recent first)
    borrowed_books_data.sort(
        key=lambda book: datetime.strptime(book['borrowed_date'], '%d-%m-%Y %H:%M:%S'), 
        reverse=True
    )
        
    # Now converting to "time ago" format
    for book in borrowed_books_data:
        book['borrowed_date'] = time_ago(book['borrowed_date'])

    # borrowed_books_data.sort(key=lambda book: book['borrowed_date']) 

    return render_template('admin/adminDashboard.html', 
                           admin_user = admin_user,
                           library_users = library_users,
                           library_books = library_books,
                           active_page='adminDashboard',
                           borrowed_books_data = borrowed_books_data                          
                           )

@app.route('/admin/add_books', methods=['GET', 'POST'])
@login_required
@admin_required
def add_books():
    form = AddBookForm()

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        isbn = form.isbn.data
        available_copies = form.copies.data
        total_copies = available_copies

        # creating and instance of class Book to add new book
        new_book = Book(title, author, isbn, available_copies, total_copies)
        

        # adding a new book, using the add_book function from helper.py
        add_book(library, new_book)

        # saving the added book to json storage   
        save_books(library) 

        flash('Book added successfully!', 'success')
        return redirect(url_for('adminDashboard'))
    flash('Book ISBN Already Exist', 'fail')


    return render_template("/admin/add_books.html", form=form,
                           admin_user = admin_user, active_page='add_books')


@app.route('/admin/manage_users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    library_users = load_users(library)
    library_users = [user.to_dict() for user in library_users.values()]

    library_users.sort(key=lambda user: user['name'])
    


    return render_template("admin/manage_users.html", 
                           library_users = library_users,
                           admin_user = admin_user,
                           active_page = "manage_users"
                           )

@app.route('/admin/delete/<user_id>')
@login_required
@admin_required
def delete_users(user_id):

    load_user(library)
    delete_user(library, user_id)
    save_users(library)

    return redirect(url_for("manage_users"))

@app.route('/admin/edit/<user_id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_users(user_id):
    load_user(library)
    user = get_user_by_id(library, user_id)
    print(user)

    full_name = user.name.strip()
    name_parts = full_name.split()

    first_name = name_parts[0]
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""  # handle middle names or no last name


    form = UpdateUserForm()

    if form.validate_on_submit():
        firstName = form.firstName.data
        lastName = form.lastName.data
        new_email = form.email.data

        new_name = firstName + " " + lastName

        edit_user(library, user.user_id, new_name, new_email)

        save_users(library)

        flash('User Details Updated successfully!', 'success')
        return redirect(url_for('manage_users'))
    flash('Email Already Exist', 'fail')
    
    return render_template("/admin/edit_user.html", user = user, admin_user = admin_user, 
                           form = form, firstName = first_name, lastName = last_name
                           )

@app.route('/admin/manage_books', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_books():
    library_books = load_books(library)
    library_books = [book.to_dict() for book in library_books.values()]

    library_books.sort(key=lambda book: book['title'])


    return render_template("admin/manage_books.html", 
                           library_books = library_books,
                           admin_user = admin_user,
                           active_page = "manage_books"
                           )

@app.route('/admin/remove_book/<isbn>')
@login_required
@admin_required
def remove_books(isbn):
    
    load_books(library)
    remove_book(library, isbn)
    save_books(library)

    return redirect(url_for("manage_books"))

@app.route('/admin/edit_book/<isbn>', methods = ['GET', 'POST'])
@login_required
@admin_required
def edit_books(isbn):
    load_books(library)
    book = get_book_by_isbn(library, isbn)
    print(book)

    form = UpdateBookForm()

    if form.validate_on_submit():
        new_isbn = form.isbn.data
        new_title = form.title.data
        new_author = form.author.data
        updated_copies = form.copies.data

        new_available_copies = book.available_copies + updated_copies
        new_total_copies = book.total_copies + updated_copies


        edit_book(library, book.isbn, new_isbn, new_title, new_author, new_available_copies, new_total_copies)

        save_books(library)

        flash('Book Details Updated successfully!', 'success')
        return redirect(url_for('manage_books'))
    flash('Book Details Already Exist', 'fail')
    
    return render_template("/admin/edit_book.html", book = book, admin_user = admin_user, 
                           form = form
                           )

@app.route('/admin/search_user', methods = ['GET', 'POST'])
@login_required
@admin_required
def search_user():
    form = SearchUserForm()
    users = []

    if form.validate_on_submit():
        name = form.name.data
        users = search_users(library, name)
        # print(users)

        for user in users:
            print(user)

        return render_template('admin/search_users.html', admin_user=admin_user, form=form, users=users, active_page = 'search_user') 


    return render_template('admin/search_users.html', admin_user=admin_user, form=form, users=users, active_page = 'search_user')

@app.route('/admin/user_details/<user_id>', methods = ['GET', 'POST'])
@login_required
@admin_required
def user_details(user_id):
    load_user(library)
    user = get_user_by_id(library, user_id)
    print(user)

    return render_template('/admin/user_details.html', user = user, admin_user=admin_user)

@app.route('/admin/search_book', methods = ['GET', 'POST'])
@login_required
@admin_required
def search_book():
    form = SearchBookForm()
    books = []

    if form.validate_on_submit():
        title = form.title.data
        books = search_books(library, title)

        for book in books:
            print(book)

        return render_template('admin/search_book.html', admin_user=admin_user, form=form, books=books, active_page = 'search_book') 


    return render_template('admin/search_book.html', admin_user=admin_user, form=form, books=books, active_page = 'search_book')

@app.route('/admin/book_details/<isbn>', methods = ['GET', 'POST'])
@login_required
@admin_required
def book_details(isbn):
    load_books(library)
    book = get_book_by_isbn(library, isbn)
    print(book)

    return render_template('/admin/book_details.html', book = book, admin_user=admin_user)

@app.route('/admin/borrowed_books_history', methods = ['GET', 'POST'])
@login_required
@admin_required
def borrowed_books_history():

    library_users = load_users(library)
    library_books = load_books(library)

    library_users = [user.to_dict() for user in library_users.values()]
    library_books = [book.to_dict() for book in library_books.values()]

    borrowed_books_data = []

    for user in library_users:
        for borrowed in user['borrowed_books']:
            for book in library_books:
                if borrowed['isbn'] == book['isbn']:
                    data = {
                        'name': user['name'],
                        'title': book['title'],
                        'isbn': borrowed['isbn'],
                        'user_id': user['user_id'],
                        'borrowed_date': borrowed['borrowed_date'],
                        'return_date': borrowed['return_date'][:10],
                        'return_status': borrowed['returned']
                    }

                    borrowed_books_data.append(data)

                if borrowed['returned'] == True:
                    data['actual_return_date'] = borrowed['actual_return_date'][:10]


    # Sorting by the datetime (most recent first)
    borrowed_books_data.sort(
        key=lambda book: datetime.strptime(book['borrowed_date'], '%d-%m-%Y %H:%M:%S'), 
        reverse=True
    )
        
    # Now converting to "time ago" format
    for book in borrowed_books_data:
        book['borrowed_date'] = time_ago(book['borrowed_date'])

    print ('borrowed_book: ', borrowed_books_data)


    return render_template('/admin/borrowed_books_history.html', 
                           admin_user = admin_user,
                           library_users = library_users,
                           library_books = library_books,
                           active_page='borrowed_books_history',
                           borrowed_books_data = borrowed_books_data                          
                           )

@app.route('/admin/add_ebooks', methods=['GET', 'POST'])
@login_required
@admin_required
def add_ebooks():
    form = AddeBookForm()

    if form.validate_on_submit():
        title = form.title.data
        author = form.author.data
        isbn = form.isbn.data
        format = form.format.data
        file_path = form.file_path.data

        # creating and instance of class Book to add new book
        new_book = Book(title, author, isbn, format)
        

        # adding a new book, using the add_book function from helper.py
        add_book(library, new_book)

        # saving the added book to json storage   
        save_books(library) 

        flash('Book added successfully!', 'success')
        return redirect(url_for('adminDashboard'))
    flash('Book ISBN Already Exist', 'fail')


    return render_template("admin/add_books.html", form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    print(f"Logging out user: {current_user.id}")
    logout_user()  # Fixed - no parameter
    print("User logged out")
    return redirect(url_for('login'))




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)