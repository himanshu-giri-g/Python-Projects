import openai
import speech_recognition as sr
import pyttsx3
import os
import pyautogui
import webbrowser
import time

# Initialize OpenAI with your API key
openai.api_key = "your-openai-api-key"

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set up text-to-speech engine properties
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to speak out text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input from the user
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand. Please say that again.")
        return ""
    except sr.RequestError:
        speak("Sorry, I couldn't reach the speech recognition service.")
        return ""

# Function to handle OpenAI queries
def ask_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # GPT-3 model
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to search the web or open a specific website
def search_web(query):
    speak(f"Searching for {query} on the web")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Function to open specific websites directly
def open_website(site_name):
    websites = {
        'youtube': 'https://www.youtube.com',
        'google': 'https://www.google.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://www.twitter.com',
        'gmail': 'https://mail.google.com'
    }
    
    if site_name in websites:
        speak(f"Opening {site_name}")
        webbrowser.open(websites[site_name])
    else:
        speak(f"Sorry, I don't know the website for {site_name}.")

# Function to execute commands based on voice input
def execute_command(command):
    if 'open notepad' in command:
        speak('Opening Notepad')
        os.system('notepad')
    
    elif 'open browser' in command:
        speak('Opening browser')
        webbrowser.open('https://www.google.com')
    
    elif 'close notepad' in command:
        speak('Closing Notepad')
        os.system("taskkill /f /im notepad.exe")
    
    elif 'shutdown' in command:
        speak('Shutting down the system')
        os.system("shutdown /s /t 5")
    
    elif 'restart' in command:
        speak('Restarting the system')
        os.system("shutdown /r /t 5")
    
    elif 'play music' in command:
        speak('Playing music')
        music_dir = "C:\\Users\\Public\\Music\\Sample Music"  # Adjust the path to your music directory
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    
    elif 'volume up' in command:
        pyautogui.press("volumeup", presses=5)
        speak('Volume increased')
    
    elif 'volume down' in command:
        pyautogui.press("volumedown", presses=5)
        speak('Volume decreased')
    
    elif 'mute' in command:
        pyautogui.press("volumemute")
        speak('Volume muted')
    
    elif 'screenshot' in command:
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak('Screenshot taken')
    
    elif 'what is the time' in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    
    elif 'sleep' in command:
        speak('Putting the system to sleep')
        os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')

    elif 'log off' in command:
        speak('Logging off the system')
        os.system('shutdown -l')

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        if search_query:
            search_web(search_query)
        else:
            speak("What do you want to search for?")
            query = take_command()
            if query:
                search_web(query)

    elif 'open' in command:
        site_name = command.replace('open', '').strip()
        if site_name:
            open_website(site_name)
        else:
            speak("Which website would you like to open?")
    
    else:
        speak("Let me ask OpenAI for you.")
        response = ask_openai(command)
        speak(response)

# Main loop to keep listening for commands
if __name__ == "__main__":
    speak("Hello, I am JARVIS, your desktop assistant. How can I assist you today?")
    
    while True:
        command = take_command()
        if command:
            execute_command(command)
        if 'stop' in command or 'exit' in command:
            speak("Goodbye!")
            break
