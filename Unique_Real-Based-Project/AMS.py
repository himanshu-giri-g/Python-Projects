import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime

# Student class to store individual student information
class Student:
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        self.attendance = {}  # Dictionary to store attendance by date

# Function to add a new student
def add_student():
    student_id = entry_id.get()
    name = entry_name.get()
    if student_id.isdigit() and name != "":
        student = Student(int(student_id), name)
        students.append(student)
        listbox.insert(tk.END, f"ID: {student_id}, Name: {name}")
        messagebox.showinfo("Success", f"Student {name} added successfully!")
        entry_id.delete(0, tk.END)
        entry_name.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter valid Student ID and Name.")

# Function to mark attendance for a student on a specific date
def mark_attendance():
    student_id = entry_mark_id.get()
    attendance_date = calendar.get_date()
    status = attendance_status.get()

    if student_id.isdigit():
        student_id = int(student_id)
        for student in students:
            if student.id == student_id:
                student.attendance[attendance_date] = status
                messagebox.showinfo("Success", f"Attendance marked for {student.name} on {attendance_date} as {status}.")
                entry_mark_id.delete(0, tk.END)
                return
        messagebox.showwarning("Not Found", f"Student with ID {student_id} not found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a valid Student ID.")

# Function to view the attendance of all students
def view_attendance():
    if not students:
        messagebox.showinfo("No Students", "No students added yet.")
        return

    attendance_window = tk.Toplevel(root)
    attendance_window.title("Attendance Records")
    tk.Label(attendance_window, text="ID\tName\t\t\tAttendance").grid(row=0, column=0)
    tk.Label(attendance_window, text="--------------------------------------------").grid(row=1, column=0)

    for index, student in enumerate(students):
        attendance_str = ', '.join([f"{date}: {status}" for date, status in student.attendance.items()])
        tk.Label(attendance_window, text=f"{student.id}\t{student.name:20}\t{attendance_str}").grid(row=index + 2, column=0)

# Main Tkinter window setup
root = tk.Tk()
root.title("Attendance Management System")

students = []

# Frame for Adding Students
frame_add = tk.Frame(root)
frame_add.pack(pady=10)

tk.Label(frame_add, text="Add Student").grid(row=0, column=0, columnspan=2)

tk.Label(frame_add, text="Student ID: ").grid(row=1, column=0)
entry_id = tk.Entry(frame_add)
entry_id.grid(row=1, column=1)

tk.Label(frame_add, text="Name: ").grid(row=2, column=0)
entry_name = tk.Entry(frame_add)
entry_name.grid(row=2, column=1)

btn_add = tk.Button(frame_add, text="Add Student", command=add_student)
btn_add.grid(row=3, column=0, columnspan=2)

# Frame for Marking Attendance
frame_mark = tk.Frame(root)
frame_mark.pack(pady=10)

tk.Label(frame_mark, text="Mark Attendance").grid(row=0, column=0, columnspan=2)

tk.Label(frame_mark, text="Student ID: ").grid(row=1, column=0)
entry_mark_id = tk.Entry(frame_mark)
entry_mark_id.grid(row=1, column=1)

# Add Calendar widget to select date
tk.Label(frame_mark, text="Select Date: ").grid(row=2, column=0)
calendar = Calendar(frame_mark, selectmode='day', date_pattern='yyyy-mm-dd')
calendar.grid(row=2, column=1)

# Add Radio Buttons for attendance status (Present or Absent)
attendance_status = tk.StringVar()
attendance_status.set("Present")  # Default value

tk.Label(frame_mark, text="Attendance Status: ").grid(row=3, column=0)
radio_present = tk.Radiobutton(frame_mark, text="Present", variable=attendance_status, value="Present")
radio_present.grid(row=3, column=1)
radio_absent = tk.Radiobutton(frame_mark, text="Absent", variable=attendance_status, value="Absent")
radio_absent.grid(row=4, column=1)

btn_mark = tk.Button(frame_mark, text="Mark Attendance", command=mark_attendance)
btn_mark.grid(row=5, column=0, columnspan=2)

# Frame for Viewing Attendance
frame_view = tk.Frame(root)
frame_view.pack(pady=10)

btn_view = tk.Button(frame_view, text="View Attendance", command=view_attendance)
btn_view.grid(row=0, column=0)

# Frame for Displaying Students List
frame_list = tk.Frame(root)
frame_list.pack(pady=10)

listbox = tk.Listbox(frame_list, width=40)
listbox.pack()

# Start the Tkinter main loop
root.mainloop()
