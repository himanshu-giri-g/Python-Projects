import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os

FILENAME = "contacts.dat"
MAX_CONTACTS = 100
contacts = []
contact_count = 0


class Contact:
    def __init__(self, id, name, phone, email, group):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group


def load_contacts():
    global contact_count, contacts
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                contacts.append(Contact(int(row[0]), row[1], row[2], row[3], row[4]))
            contact_count = len(contacts)


def save_contacts():
    with open(FILENAME, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Phone", "Email", "Group"])
        for contact in contacts:
            writer.writerow([contact.id, contact.name, contact.phone, contact.email, contact.group])


def add_contact_window():
    def add_contact():
        global contact_count
        if contact_count >= MAX_CONTACTS:
            messagebox.showerror("Error", "Contact limit reached!")
            return

        name = name_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        group = group_entry.get()

        if not name or not phone or not email or not group:
            messagebox.showerror("Error", "All fields must be filled!")
            return

        contact = Contact(contact_count + 1, name, phone, email, group)
        contacts.append(contact)
        contact_count += 1
        save_contacts()
        messagebox.showinfo("Success", "Contact added successfully!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Contact")

    tk.Label(add_window, text="Name").grid(row=0, column=0)
    tk.Label(add_window, text="Phone").grid(row=1, column=0)
    tk.Label(add_window, text="Email").grid(row=2, column=0)
    tk.Label(add_window, text="Group").grid(row=3, column=0)

    name_entry = tk.Entry(add_window)
    phone_entry = tk.Entry(add_window)
    email_entry = tk.Entry(add_window)
    group_entry = tk.Entry(add_window)

    name_entry.grid(row=0, column=1)
    phone_entry.grid(row=1, column=1)
    email_entry.grid(row=2, column=1)
    group_entry.grid(row=3, column=1)

    tk.Button(add_window, text="Add Contact", command=add_contact).grid(row=4, column=0, columnspan=2)


def view_contacts_window():
    view_window = tk.Toplevel(root)
    view_window.title("View Contacts")

    for i, contact in enumerate(contacts):
        tk.Label(view_window, text=f"ID: {contact.id} | Name: {contact.name} | Phone: {contact.phone} | Email: {contact.email} | Group: {contact.group}").grid(row=i, column=0)


def edit_contact_window():
    def update_contact(contact, name, phone, email, group):
        if name and phone and email and group:
            contact.name = name
            contact.phone = phone
            contact.email = email
            contact.group = group
            save_contacts()
            messagebox.showinfo("Success", "Contact updated!")
            edit_window.destroy()
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def load_contact():
        id = int(id_entry.get())
        for contact in contacts:
            if contact.id == id:
                tk.Label(edit_window, text="Name").grid(row=2, column=0)
                tk.Label(edit_window, text="Phone").grid(row=3, column=0)
                tk.Label(edit_window, text="Email").grid(row=4, column=0)
                tk.Label(edit_window, text="Group").grid(row=5, column=0)

                name_entry = tk.Entry(edit_window)
                phone_entry = tk.Entry(edit_window)
                email_entry = tk.Entry(edit_window)
                group_entry = tk.Entry(edit_window)

                name_entry.insert(0, contact.name)
                phone_entry.insert(0, contact.phone)
                email_entry.insert(0, contact.email)
                group_entry.insert(0, contact.group)

                name_entry.grid(row=2, column=1)
                phone_entry.grid(row=3, column=1)
                email_entry.grid(row=4, column=1)
                group_entry.grid(row=5, column=1)

                tk.Button(edit_window, text="Save Changes", command=lambda: update_contact(contact, name_entry.get(), phone_entry.get(), email_entry.get(), group_entry.get())).grid(row=6, column=0, columnspan=2)

                return
        messagebox.showerror("Error", "Contact not found!")

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Contact")

    tk.Label(edit_window, text="Enter Contact ID").grid(row=0, column=0)
    id_entry = tk.Entry(edit_window)
    id_entry.grid(row=0, column=1)

    tk.Button(edit_window, text="Find Contact", command=load_contact).grid(row=1, column=0, columnspan=2)


def delete_contact_window():
    def delete_contact():
        id = int(id_entry.get())
        for i, contact in enumerate(contacts):
            if contact.id == id:
                contacts.pop(i)
                save_contacts()
                messagebox.showinfo("Success", "Contact deleted!")
                delete_window.destroy()
                return
        messagebox.showerror("Error", "Contact not found!")

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Contact")

    tk.Label(delete_window, text="Enter Contact ID").grid(row=0, column=0)
    id_entry = tk.Entry(delete_window)
    id_entry.grid(row=0, column=1)

    tk.Button(delete_window, text="Delete Contact", command=delete_contact).grid(row=1, column=0, columnspan=2)


def search_contact_window():
    def search_contact():
        term = search_entry.get()
        results_window = tk.Toplevel(search_window)
        results_window.title("Search Results")

        found = False
        for contact in contacts:
            if term.lower() in contact.name.lower():
                tk.Label(results_window, text=f"ID: {contact.id} | Name: {contact.name} | Phone: {contact.phone} | Email: {contact.email} | Group: {contact.group}").grid()
                found = True
        if not found:
            tk.Label(results_window, text="No contact found!").grid()

    search_window = tk.Toplevel(root)
    search_window.title("Search Contact")

    tk.Label(search_window, text="Enter name to search: ").grid(row=0, column=0)
    search_entry = tk.Entry(search_window)
    search_entry.grid(row=0, column=1)

    tk.Button(search_window, text="Search", command=search_contact).grid(row=1, column=0, columnspan=2)


# Initialize the main application window
root = tk.Tk()
root.title("Contact Management System")

# Main buttons
tk.Button(root, text="Add Contact", width=20, command=add_contact_window).grid(row=0, column=0)
tk.Button(root, text="View Contacts", width=20, command=view_contacts_window).grid(row=1, column=0)
tk.Button(root, text="Edit Contact", width=20, command=edit_contact_window).grid(row=2, column=0)
tk.Button(root, text="Delete Contact", width=20, command=delete_contact_window).grid(row=3, column=0)
tk.Button(root, text="Search Contact", width=20, command=search_contact_window).grid(row=4, column=0)

load_contacts()

# Run the GUI main loop
root.mainloop()
