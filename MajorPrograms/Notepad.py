import tkinter as tk
from tkinter import filedialog, messagebox, font, simpledialog, StringVar
from tkinter.scrolledtext import ScrolledText
import os
import time
import pyperclip
from datetime import datetime
from cryptography.fernet import Fernet
from tkinter import font as tkFont

class AdvancedNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Notepad")
        self.root.geometry("800x600")
        self.file_path = None
        self.theme_colors = {"bg": "white", "fg": "black"}
        self.auto_save_interval = 30000

        # Create a variable for font selection
        self.font_family = StringVar(value="Arial")

        # Set up the Text widget with a scroll bar
        self.text_area = ScrolledText(self.root, undo=True, wrap="word", font=("Arial", 12))
        self.text_area.pack(fill=tk.BOTH, expand=1)

        # Line number widget
        self.line_numbers = tk.Text(self.root, width=4, padx=3, takefocus=0, border=0, background='lightgray', state='disabled')
        self.line_numbers.pack(side="left", fill=tk.Y)

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_command(label="Save as PDF", command=self.save_as_pdf)
        self.file_menu.add_command(label="Print", command=self.print_file)
        self.file_menu.add_command(label="Open Recent", command=self.open_recent_files)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_exit)

        # Add edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_command(label="Select All", command=self.select_all_text)
        self.edit_menu.add_command(label="Find & Replace", command=self.find_replace)
        self.edit_menu.add_command(label="Find using Regex", command=self.find_with_regex)

        # Add view menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.show_line_numbers = tk.BooleanVar()
        self.show_line_numbers.set(False)
        self.view_menu.add_checkbutton(label="Show Line Numbers", onvalue=True, offvalue=False, variable=self.show_line_numbers, command=self.toggle_line_numbers)
        self.show_status_bar = tk.BooleanVar()
        self.show_status_bar.set(True)
        self.view_menu.add_checkbutton(label="Show Status Bar", onvalue=True, offvalue=False, variable=self.show_status_bar, command=self.toggle_status_bar)
        self.view_menu.add_command(label="Dark Mode", command=self.apply_dark_mode)
        self.view_menu.add_command(label="Light Mode", command=self.apply_light_mode)
        self.view_menu.add_command(label="Change Theme Color", command=self.change_theme_color)

        # Add format menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)

        # Font dropdown
        font_options = ["Arial", "Courier New", "Times New Roman", "Helvetica", "Verdana"]
        self.font_dropdown = tk.OptionMenu(self.root, self.font_family, *font_options, command=self.change_font)
        self.font_dropdown.pack(side="top", anchor="ne")

        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italics", command=self.toggle_italics)
        self.format_menu.add_command(label="Underline", command=self.toggle_underline)

        # Add tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Word Count", command=self.word_count)
        self.tools_menu.add_command(label="Character Count", command=self.character_count)
        self.tools_menu.add_command(label="Insert Timestamp", command=self.insert_timestamp)
        self.tools_menu.add_command(label="Insert Current Date", command=self.insert_current_date)
        self.tools_menu.add_command(label="Insert Clipboard Text", command=self.insert_clipboard_text)
        self.tools_menu.add_command(label="Encrypt File", command=self.encrypt_file)
        self.tools_menu.add_command(label="Decrypt File", command=self.decrypt_file)
        self.tools_menu.add_command(label="Auto Save", command=self.toggle_auto_save)

        # Status bar
        self.status_bar = tk.Label(self.root, text="Line 1, Column 1", anchor="e")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Variables for fonts and styles
        self.current_font = font.Font(self.text_area, self.text_area.cget("font"))
        self.bold_enabled = False
        self.italic_enabled = False
        self.underline_enabled = False

        self.auto_save_enabled = False
        self.update_status_bar()

        # Bind the close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    ### Missing File Operations ###

    def new_file(self):
        self.file_path = None
        self.text_area.delete(1.0, tk.END)
        self.update_line_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.update_line_numbers()

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Success", "File saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {e}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def save_as_pdf(self):
        messagebox.showinfo("Save as PDF", "Feature to save as PDF is not implemented yet.")

    def print_file(self):
        messagebox.showinfo("Print", "Feature to print the file is not implemented yet.")

    def open_recent_files(self):
        messagebox.showinfo("Open Recent Files", "Feature to open recent files is not implemented yet.")

    ### Clipboard Operations ###

    def cut_text(self):
        try:
            self.copy_text()
            self.text_area.delete("sel.first", "sel.last")
        except tk.TclError:
            messagebox.showwarning("Warning", "No text selected to cut.")

    def copy_text(self):
        try:
            selected_text = self.text_area.get("sel.first", "sel.last")
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            messagebox.showwarning("Warning", "No text selected to copy.")

    def paste_text(self):
        clipboard_text = self.root.clipboard_get()
        self.text_area.insert(tk.INSERT, clipboard_text)

    def select_all_text(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)

    ### Find & Replace ###

    def find_replace(self):
        messagebox.showinfo("Find & Replace", "Feature to find and replace text is not implemented yet.")

    def find_with_regex(self):
        messagebox.showinfo("Find with Regex", "Feature to find using regex is not implemented yet.")

    ### Word/Character Count ###

    def word_count(self):
        text = self.text_area.get(1.0, tk.END)
        word_count = len(text.split())
        messagebox.showinfo("Word Count", f"Words: {word_count}")

    def character_count(self):
        text = self.text_area.get(1.0, tk.END)
        char_count = len(text) - 1
        messagebox.showinfo("Character Count", f"Characters: {char_count}")

    ### Timestamp/Clipboard Insertion ###

    def insert_timestamp(self):
        current_time = time.strftime("%H:%M:%S")
        self.text_area.insert(tk.INSERT, current_time)

    def insert_current_date(self):
        current_date = time.strftime("%Y-%m-%d")
        self.text_area.insert(tk.INSERT, current_date)

    def insert_clipboard_text(self):
        clipboard_text = pyperclip.paste()
        self.text_area.insert(tk.INSERT, clipboard_text)

    ### Encryption & Decryption ###

    def encrypt_file(self):
        if self.file_path:
            key = Fernet.generate_key()
            cipher = Fernet(key)
            with open(self.file_path, "rb") as file:
                data = file.read()
            encrypted_data = cipher.encrypt(data)
            with open(self.file_path, "wb") as file:
                file.write(encrypted_data)
            messagebox.showinfo("Encryption", "File encrypted successfully.")
        else:
            messagebox.showwarning("Error", "No file to encrypt.")

    def decrypt_file(self):
        if self.file_path:
            key = simpledialog.askstring("Input", "Enter the encryption key:")
            if key:
                cipher = Fernet(key.encode())
                try:
                    with open(self.file_path, "rb") as file:
                        data = file.read()
                    decrypted_data = cipher.decrypt(data)
                    with open(self.file_path, "wb") as file:
                        file.write(decrypted_data)
                    messagebox.showinfo("Decryption", "File decrypted successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to decrypt the file: {e}")
        else:
            messagebox.showwarning("Error", "No file to decrypt.")

    ### Auto-Save ###

    def toggle_auto_save(self):
        self.auto_save_enabled = not self.auto_save_enabled
        if self.auto_save_enabled:
            self.auto_save()
            messagebox.showinfo("Auto Save", "Auto save enabled.")
        else:
            messagebox.showinfo("Auto Save", "Auto save disabled.")

    def auto_save(self):
        if self.auto_save_enabled:
            self.save_file()
            self.root.after(self.auto_save_interval, self.auto_save)

    ### Helper Methods ###

    def toggle_line_numbers(self):
        if self.show_line_numbers.get():
            self.line_numbers.pack(side="left", fill=tk.Y)
        else:
            self.line_numbers.pack_forget()

    def toggle_status_bar(self):
        if self.show_status_bar.get():
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            self.status_bar.pack_forget()

    def apply_dark_mode(self):
        self.text_area.config(bg="black", fg="white")
        self.status_bar.config(bg="black", fg="white")

    def apply_light_mode(self):
        self.text_area.config(bg="white", fg="black")
        self.status_bar.config(bg="white", fg="black")

    def change_theme_color(self):
        pass

    def toggle_bold(self):
        if self.bold_enabled:
            self.current_font.config(weight="normal")
        else:
            self.current_font.config(weight="bold")
        self.bold_enabled = not self.bold_enabled
        self.text_area.config(font=self.current_font)

    def toggle_italics(self):
        if self.italic_enabled:
            self.current_font.config(slant="roman")
        else:
            self.current_font.config(slant="italic")
        self.italic_enabled = not self.italic_enabled
        self.text_area.config(font=self.current_font)

    def toggle_underline(self):
        if self.underline_enabled:
            self.current_font.config(underline=0)
        else:
            self.current_font.config(underline=1)
        self.underline_enabled = not self.underline_enabled
        self.text_area.config(font=self.current_font)

    def change_font(self, _):
        selected_font = self.font_family.get()
        self.text_area.config(font=(selected_font, self.current_font.actual('size')))

    def update_status_bar(self):
        line, col = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Line {line}, Column {col}")
        self.text_area.bind('<KeyRelease>', lambda e: self.update_status_bar())

    def update_line_numbers(self):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state=tk.DISABLED)

    def on_exit(self):
        if self.file_path and self.text_area.get(1.0, tk.END).strip():
            response = messagebox.askyesnocancel("Confirm Exit", "Do you want to save changes?")
            if response:  # Yes
                self.save_file()
            elif response is None:  # Cancel
                return
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedNotepad(root)
    root.mainloop()
