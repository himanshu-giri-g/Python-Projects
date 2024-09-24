import tkinter as tk
from tkinter import messagebox
import time

# Create the main window
root = tk.Tk()
root.title("Digital Clock with Stopwatch, Alarm, and Timer")
root.geometry("400x400")

# Global variables for Alarm and Timer
alarm_set_time = None
timer_running = False
stopwatch_running = False
stopwatch_counter = 0
timer_counter = 0

# Function to update the digital clock
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    
    # Check for alarm
    global alarm_set_time
    if alarm_set_time and current_time == alarm_set_time:
        messagebox.showinfo("Alarm", "Wake Up! Time's up!")
        alarm_set_time = None  # Reset alarm after it goes off
    
    clock_label.after(1000, update_clock)

# Function to set an alarm
def set_alarm():
    global alarm_set_time
    alarm_set_time = alarm_entry.get()
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_set_time}")
    alarm_entry.delete(0, tk.END)

# Function for stopwatch
def run_stopwatch():
    global stopwatch_running, stopwatch_counter
    if stopwatch_running:
        minutes, seconds = divmod(stopwatch_counter, 60)
        hours, minutes = divmod(minutes, 60)
        time_format = f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
        stopwatch_label.config(text=time_format)
        stopwatch_counter += 1
        stopwatch_label.after(1000, run_stopwatch)

def start_stopwatch():
    global stopwatch_running
    if not stopwatch_running:
        stopwatch_running = True
        run_stopwatch()

def stop_stopwatch():
    global stopwatch_running
    stopwatch_running = False

def reset_stopwatch():
    global stopwatch_counter, stopwatch_running
    stopwatch_running = False
    stopwatch_counter = 0
    stopwatch_label.config(text="00:00:00")

# Function for timer
def run_timer():
    global timer_counter, timer_running
    if timer_running and timer_counter >= 0:
        minutes, seconds = divmod(timer_counter, 60)
        time_format = f'{int(minutes):02d}:{int(seconds):02d}'
        timer_label.config(text=time_format)
        timer_counter -= 1
        timer_label.after(1000, run_timer)
    elif timer_counter < 0:
        messagebox.showinfo("Timer", "Time's up!")
        timer_running = False

def start_timer():
    global timer_running, timer_counter
    if not timer_running:
        hours = hours_var.get()
        minutes = minutes_var.get()
        seconds = seconds_var.get()
        timer_counter = hours * 3600 + minutes * 60 + seconds
        timer_running = True
        run_timer()

def stop_timer():
    global timer_running
    timer_running = False

def reset_timer():
    global timer_counter, timer_running
    timer_running = False
    timer_counter = 0
    timer_label.config(text="00:00")

# ---------------- GUI Layout ----------------

# Digital Clock
clock_label = tk.Label(root, text="", font=("Helvetica", 48), bg="black", fg="cyan")
clock_label.pack(pady=20)

# Alarm Section
alarm_frame = tk.Frame(root)
alarm_frame.pack(pady=10)

alarm_label = tk.Label(alarm_frame, text="Set Alarm (HH:MM:SS):")
alarm_label.pack(side=tk.LEFT)

alarm_entry = tk.Entry(alarm_frame)
alarm_entry.pack(side=tk.LEFT)

set_alarm_button = tk.Button(alarm_frame, text="Set Alarm", command=set_alarm)
set_alarm_button.pack(side=tk.LEFT)

# Stopwatch Section
stopwatch_frame = tk.Frame(root)
stopwatch_frame.pack(pady=10)

stopwatch_label = tk.Label(stopwatch_frame, text="00:00:00", font=("Helvetica", 24))
stopwatch_label.pack()

start_stopwatch_button = tk.Button(stopwatch_frame, text="Start", command=start_stopwatch)
start_stopwatch_button.pack(side=tk.LEFT)

stop_stopwatch_button = tk.Button(stopwatch_frame, text="Stop", command=stop_stopwatch)
stop_stopwatch_button.pack(side=tk.LEFT)

reset_stopwatch_button = tk.Button(stopwatch_frame, text="Reset", command=reset_stopwatch)
reset_stopwatch_button.pack(side=tk.LEFT)

# Timer Section
timer_frame = tk.Frame(root)
timer_frame.pack(pady=10)

timer_label = tk.Label(timer_frame, text="00:00", font=("Helvetica", 24))
timer_label.pack()

# Dropdowns for hours, minutes, and seconds
hours_var = tk.IntVar(value=0)
minutes_var = tk.IntVar(value=0)
seconds_var = tk.IntVar(value=0)

hours_label = tk.Label(timer_frame, text="Hours:")
hours_label.pack(side=tk.LEFT)
hours_dropdown = tk.OptionMenu(timer_frame, hours_var, *range(0, 25))
hours_dropdown.pack(side=tk.LEFT)

minutes_label = tk.Label(timer_frame, text="Minutes:")
minutes_label.pack(side=tk.LEFT)
minutes_dropdown = tk.OptionMenu(timer_frame, minutes_var, *range(0, 60))
minutes_dropdown.pack(side=tk.LEFT)

seconds_label = tk.Label(timer_frame, text="Seconds:")
seconds_label.pack(side=tk.LEFT)
seconds_dropdown = tk.OptionMenu(timer_frame, seconds_var, *range(0, 60))
seconds_dropdown.pack(side=tk.LEFT)

start_timer_button = tk.Button(timer_frame, text="Start Timer", command=start_timer)
start_timer_button.pack(side=tk.LEFT)

stop_timer_button = tk.Button(timer_frame, text="Stop", command=stop_timer)
stop_timer_button.pack(side=tk.LEFT)

reset_timer_button = tk.Button(timer_frame, text="Reset", command=reset_timer)
reset_timer_button.pack(side=tk.LEFT)

# Start updating the clock
update_clock()

# Start the main event loop
root.mainloop()
