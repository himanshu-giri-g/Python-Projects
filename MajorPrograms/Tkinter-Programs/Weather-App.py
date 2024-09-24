import tkinter as tk
from tkinter import messagebox
import requests

# Function to fetch weather data
def get_weather():
    api_key = "91cf9df4f9cdb92a6ab2a86a1e5ecb68"  # Replace with your OpenWeatherMap API key
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        print(response.status_code)  # Debugging line
        print(response.json())       # Debugging line

        if response.status_code == 200:
            data = response.json()  # Get JSON data from response
            temperature = data['main']['temp']
            weather_desc = data['weather'][0]['description']
            result_label.config(text=f"Temperature: {temperature}°C\nDescription: {weather_desc.capitalize()}")
        else:
            messagebox.showerror("Error", data['message'])
    
    except Exception as e:
        messagebox.showerror("Error", "Could not fetch weather data. Please try again.")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("300x200")

# GUI Layout
city_label = tk.Label(root, text="Enter City Name:")
city_label.pack(pady=10)

city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

get_weather_button = tk.Button(root, text="Get Weather", command=get_weather)
get_weather_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# Start the main event loop
root.mainloop()
