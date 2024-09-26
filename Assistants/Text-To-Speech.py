import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to convert text to speech
def text_to_speech(text):
    # Set properties before speaking (optional)
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

    # Pass the text to be spoken
    engine.say(text)

    # Run the speech engine
    engine.runAndWait()

# Test the function
if __name__ == "__main__":
    # Input text
    text = input("Enter the text you want to convert to speech: ")

    # Call the function to speak the text
    text_to_speech(text)
