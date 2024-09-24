import tkinter as tk
from tkinter import messagebox, simpledialog

class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.reserved_by = None

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.borrowed_books = []
        self.borrow_count = 0
        self.fines_due = 0.0
        self.history = []

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        
        self.books = []
        self.users = []
        self.book_count = 0
        self.user_count = 0
        
        self.initialize()
        self.create_main_menu()

    def initialize(self):
        self.add_book("The Great Gatsby", "F. Scott Fitzgerald")
        self.add_book("1984", "George Orwell")
        self.add_user("admin")
    
    def create_main_menu(self):
        tk.Label(self.root, text="Library Management System", font=("Arial", 20)).pack(pady=10)

        tk.Button(self.root, text="Add Book", width=25, command=self.add_book_window).pack(pady=5)
        tk.Button(self.root, text="List Books", width=25, command=self.list_books_window).pack(pady=5)
        tk.Button(self.root, text="Search Book", width=25, command=self.search_book_window).pack(pady=5)
        tk.Button(self.root, text="Borrow Book", width=25, command=self.borrow_book_window).pack(pady=5)
        tk.Button(self.root, text="Return Book", width=25, command=self.return_book_window).pack(pady=5)
        tk.Button(self.root, text="Add User", width=25, command=self.add_user_window).pack(pady=5)
        tk.Button(self.root, text="View Users", width=25, command=self.view_users_window).pack(pady=5)
        tk.Button(self.root, text="Exit", width=25, command=self.root.quit).pack(pady=5)
    
    def add_book(self, title, author):
        self.book_count += 1
        new_book = Book(self.book_count, title, author)
        self.books.append(new_book)

    def add_user(self, username):
        self.user_count += 1
        new_user = User(self.user_count, username)
        self.users.append(new_user)

    def list_books_window(self):
        list_window = tk.Toplevel(self.root)
        list_window.title("List of Books")
        
        if not self.books:
            tk.Label(list_window, text="No books available.").pack()
        else:
            for book in self.books:
                book_info = f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Borrowed: {'Yes' if book.is_borrowed else 'No'}"
                tk.Label(list_window, text=book_info).pack()

    def add_book_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add a Book")

        tk.Label(add_window, text="Enter Book Title:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Enter Book Author:").pack()
        author_entry = tk.Entry(add_window)
        author_entry.pack()

        def save_book():
            title = title_entry.get()
            author = author_entry.get()
            if title and author:
                self.add_book(title, author)
                messagebox.showinfo("Success", "Book added successfully!")
                add_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please provide both title and author.")
        
        tk.Button(add_window, text="Save Book", command=save_book).pack(pady=10)

    def search_book_window(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Book")

        tk.Label(search_window, text="Enter Book Title to Search:").pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()

        def search():
            title = search_entry.get()
            results = [book for book in self.books if title.lower() in book.title.lower()]
            if results:
                for book in results:
                    book_info = f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Borrowed: {'Yes' if book.is_borrowed else 'No'}"
                    tk.Label(search_window, text=book_info).pack()
            else:
                tk.Label(search_window, text="No books found with that title.").pack()

        tk.Button(search_window, text="Search", command=search).pack(pady=10)

    def borrow_book_window(self):
        borrow_window = tk.Toplevel(self.root)
        borrow_window.title("Borrow Book")

        tk.Label(borrow_window, text="Enter Book ID to Borrow:").pack()
        book_id_entry = tk.Entry(borrow_window)
        book_id_entry.pack()

        tk.Label(borrow_window, text="Enter Your User ID:").pack()
        user_id_entry = tk.Entry(borrow_window)
        user_id_entry.pack()

        def borrow():
            book_id = int(book_id_entry.get())
            user_id = int(user_id_entry.get())
            book = next((b for b in self.books if b.id == book_id), None)
            user = next((u for u in self.users if u.id == user_id), None)
            if book and user:
                if not book.is_borrowed:
                    book.is_borrowed = True
                    user.borrowed_books.append(book.id)
                    user.history.append(book.id)
                    user.borrow_count += 1
                    messagebox.showinfo("Success", "Book borrowed successfully!")
                    borrow_window.destroy()
                else:
                    messagebox.showerror("Error", "Book is already borrowed.")
            else:
                messagebox.showerror("Error", "Invalid Book or User ID.")
        
        tk.Button(borrow_window, text="Borrow", command=borrow).pack(pady=10)

    def return_book_window(self):
        return_window = tk.Toplevel(self.root)
        return_window.title("Return Book")

        tk.Label(return_window, text="Enter Book ID to Return:").pack()
        book_id_entry = tk.Entry(return_window)
        book_id_entry.pack()

        def return_book():
            book_id = int(book_id_entry.get())
            book = next((b for b in self.books if b.id == book_id), None)
            if book and book.is_borrowed:
                book.is_borrowed = False
                messagebox.showinfo("Success", "Book returned successfully!")
                return_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid Book ID or the book is not borrowed.")
        
        tk.Button(return_window, text="Return", command=return_book).pack(pady=10)

    def add_user_window(self):
        add_user_window = tk.Toplevel(self.root)
        add_user_window.title("Add User")

        tk.Label(add_user_window, text="Enter Username:").pack()
        username_entry = tk.Entry(add_user_window)
        username_entry.pack()

        def save_user():
            username = username_entry.get()
            if username:
                self.add_user(username)
                messagebox.showinfo("Success", "User added successfully!")
                add_user_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please provide a username.")
        
        tk.Button(add_user_window, text="Save User", command=save_user).pack(pady=10)

    def view_users_window(self):
        users_window = tk.Toplevel(self.root)
        users_window.title("Users")

        if not self.users:
            tk.Label(users_window, text="No users available.").pack()
        else:
            for user in self.users:
                user_info = f"ID: {user.id}, Username: {user.username}, Fines Due: {user.fines_due}"
                tk.Label(users_window, text=user_info).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()
