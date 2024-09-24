import tkinter as tk
from tkinter import messagebox, filedialog
import csv
import os

MAX_STUDENTS = 100
students = []
student_count = 0

class Student:
    def __init__(self, id, name, course, age, grade):
        self.id = id
        self.name = name
        self.course = course
        self.age = age
        self.grade = grade

def add_student():
    global student_count
    if student_count >= MAX_STUDENTS:
        messagebox.showerror("Limit Reached", "Cannot add more students")
        return

    try:
        name = entry_name.get()
        course = entry_course.get()
        age = int(entry_age.get())
        grade = float(entry_grade.get())

        student = Student(student_count + 1, name, course, age, grade)
        students.append(student)
        student_count += 1

        messagebox.showinfo("Success", "Student added successfully!")
        refresh_student_list()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid age and grade")

def refresh_student_list():
    listbox_students.delete(0, tk.END)
    for student in students:
        listbox_students.insert(tk.END, f"ID: {student.id} | Name: {student.name} | Course: {student.course} | Age: {student.age} | Grade: {student.grade:.2f}")

def view_students():
    refresh_student_list()

def edit_student():
    try:
        selected = listbox_students.curselection()[0]
        student = students[selected]
        
        student.name = entry_name.get()
        student.course = entry_course.get()
        student.age = int(entry_age.get())
        student.grade = float(entry_grade.get())
        
        refresh_student_list()
        messagebox.showinfo("Success", "Student details updated")
    except IndexError:
        messagebox.showerror("Selection Error", "Please select a student to edit")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid age and grade")

def delete_student():
    try:
        selected = listbox_students.curselection()[0]
        del students[selected]
        global student_count
        student_count -= 1
        refresh_student_list()
        messagebox.showinfo("Success", "Student deleted")
    except IndexError:
        messagebox.showerror("Selection Error", "Please select a student to delete")

def save_students_to_file():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Course", "Age", "Grade"])
        for student in students:
            writer.writerow([student.id, student.name, student.course, student.age, student.grade])
    messagebox.showinfo("Success", "Students saved to students.csv")

def load_students_from_file():
    if os.path.exists("students.csv"):
        with open("students.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            global student_count
            student_count = 0
            students.clear()
            for row in reader:
                id, name, course, age, grade = int(row[0]), row[1], row[2], int(row[3]), float(row[4])
                students.append(Student(id, name, course, age, grade))
                student_count += 1
        refresh_student_list()
        messagebox.showinfo("Success", "Students loaded from students.csv")
    else:
        messagebox.showinfo("No Data", "No saved student data found")

# Tkinter GUI Setup
root = tk.Tk()
root.title("Student Management System")

frame_main = tk.Frame(root)
frame_main.pack(padx=10, pady=10)

# Input fields
tk.Label(frame_main, text="Name:").grid(row=0, column=0)
entry_name = tk.Entry(frame_main)
entry_name.grid(row=0, column=1)

tk.Label(frame_main, text="Course:").grid(row=1, column=0)
entry_course = tk.Entry(frame_main)
entry_course.grid(row=1, column=1)

tk.Label(frame_main, text="Age:").grid(row=2, column=0)
entry_age = tk.Entry(frame_main)
entry_age.grid(row=2, column=1)

tk.Label(frame_main, text="Grade:").grid(row=3, column=0)
entry_grade = tk.Entry(frame_main)
entry_grade.grid(row=3, column=1)

# Buttons
btn_add = tk.Button(frame_main, text="Add Student", command=add_student)
btn_add.grid(row=4, column=0, columnspan=2)

btn_edit = tk.Button(frame_main, text="Edit Student", command=edit_student)
btn_edit.grid(row=5, column=0, columnspan=2)

btn_delete = tk.Button(frame_main, text="Delete Student", command=delete_student)
btn_delete.grid(row=6, column=0, columnspan=2)

btn_view = tk.Button(frame_main, text="View Students", command=view_students)
btn_view.grid(row=7, column=0, columnspan=2)

btn_save = tk.Button(frame_main, text="Save to CSV", command=save_students_to_file)
btn_save.grid(row=8, column=0, columnspan=2)

btn_load = tk.Button(frame_main, text="Load from CSV", command=load_students_from_file)
btn_load.grid(row=9, column=0, columnspan=2)

# Student listbox
listbox_students = tk.Listbox(root, width=60, height=15)
listbox_students.pack(padx=10, pady=10)

# Start the application
root.mainloop()
