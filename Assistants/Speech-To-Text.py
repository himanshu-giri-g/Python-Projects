import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Function to convert speech to text
def speech_to_text():
    try:
        # Use the microphone as source for input.
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")

            # Listen for the user's input
            audio = recognizer.listen(source)

            # Use Google's speech recognition to convert audio to text
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")

            return text

    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError:
        print("Sorry, I could not request results from the speech recognition service.")

# Run the function
if __name__ == "__main__":
    print("Say something to convert to text:")
    speech_to_text()
