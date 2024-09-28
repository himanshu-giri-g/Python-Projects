import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Employee class to store information
class Employee:
    def __init__(self, emp_id, name, department, base_salary, years_of_service):
        self.id = emp_id
        self.name = name
        self.department = department
        self.base_salary = base_salary
        self.years_of_service = years_of_service
        self.bonus = 0
        self.total_salary = 0
        self.calculate_salary()

    def calculate_bonus(self):
        if self.years_of_service > 10:
            self.bonus = self.base_salary * 0.10
        elif self.years_of_service > 5:
            self.bonus = self.base_salary * 0.05
        else:
            self.bonus = 0

    def calculate_salary(self):
        self.calculate_bonus()
        self.total_salary = self.base_salary + self.bonus

# Global Employee List
employees = []

# Function to add employee to the list
def add_employee():
    try:
        emp_id = int(emp_id_entry.get())
        name = name_entry.get()
        department = dept_entry.get()
        base_salary = float(salary_entry.get())
        years_of_service = int(service_entry.get())

        new_employee = Employee(emp_id, name, department, base_salary, years_of_service)
        employees.append(new_employee)

        messagebox.showinfo("Success", "Employee added successfully!")
        clear_entries()
        refresh_employee_table()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid data.")

def clear_entries():
    emp_id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    dept_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    service_entry.delete(0, tk.END)

def refresh_employee_table():
    for row in employee_table.get_children():
        employee_table.delete(row)

    for emp in employees:
        employee_table.insert('', 'end', values=(emp.id, emp.name, emp.department, emp.base_salary, emp.years_of_service, emp.bonus, emp.total_salary))

def delete_employee():
    selected = employee_table.selection()
    if selected:
        emp_id = employee_table.item(selected[0], 'values')[0]
        for emp in employees:
            if emp.id == int(emp_id):
                employees.remove(emp)
                break
        refresh_employee_table()
        messagebox.showinfo("Success", "Employee deleted successfully.")
    else:
        messagebox.showerror("Error", "Please select an employee to delete.")

def edit_employee():
    selected = employee_table.selection()
    if selected:
        emp_id = employee_table.item(selected[0], 'values')[0]
        for emp in employees:
            if emp.id == int(emp_id):
                emp.name = name_entry.get()
                emp.department = dept_entry.get()
                emp.base_salary = float(salary_entry.get())
                emp.years_of_service = int(service_entry.get())
                emp.calculate_salary()
                break
        refresh_employee_table()
        messagebox.showinfo("Success", "Employee updated successfully.")
    else:
        messagebox.showerror("Error", "Please select an employee to edit.")

# Initialize the Tkinter window
root = tk.Tk()
root.title("Employee Management System")

# Create input fields for employee details
tk.Label(root, text="Employee ID").grid(row=0, column=0, padx=10, pady=10)
emp_id_entry = tk.Entry(root)
emp_id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Department").grid(row=2, column=0, padx=10, pady=10)
dept_entry = tk.Entry(root)
dept_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Base Salary").grid(row=3, column=0, padx=10, pady=10)
salary_entry = tk.Entry(root)
salary_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Years of Service").grid(row=4, column=0, padx=10, pady=10)
service_entry = tk.Entry(root)
service_entry.grid(row=4, column=1, padx=10, pady=10)

# Buttons for add, delete, edit functionalities
tk.Button(root, text="Add Employee", command=add_employee).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Edit Employee", command=edit_employee).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Delete Employee", command=delete_employee).grid(row=5, column=2, padx=10, pady=10)

# Create TreeView to display employees
columns = ("ID", "Name", "Department", "Base Salary", "Years of Service", "Bonus", "Total Salary")
employee_table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    employee_table.heading(col, text=col)
    employee_table.column(col, width=100)
employee_table.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

# Main loop
root.mainloop()
