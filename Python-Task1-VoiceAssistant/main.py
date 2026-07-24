import speech_recognition as sr
import pyttsx3 # The library that converts text to audio
import datetime
import webbrowser

r = sr.Recognizer()

def speak(text):
    print(f"Assistant: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait..")
        r.adjust_for_ambient_noise(source, duration=1)
        print("SPEAK NOW")

        try:
            audio = r.listen(source, timeout = 5, phrase_time_limit = 10)
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Can you repeat?")
            return""
        except sr.RequestError:
            speak("Could not request results, Check your internet connection")
            return ""
        except sr.WaitTimeoutError:
            speak("You didn't say anything please try again")
            return ""

speak("Hello! I am your voice assistant. How can I help you?. Talk Stop or type Ctrl+C to stop the program, and add the word search, in your command, to make Assistant to search")

try:
    while True:
        command = listen()
        if command:
            if "stop" in command or "exit" in command:
                speak("Goodbye!")
                break
            elif "hello" in command:
                speak("hello there how can i help you today?")
            elif "time" in command:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                speak(f"The current time is {current_time}")
            elif "date" in command:
                current_date = datetime.datetime.now().strftime("%B %d, %Y")
                speak(f"Today's date is {current_date}")
            elif "search" in command:
                topic = command.replace("search", "").strip()
                if topic:
                    speak(f"Searching the web for {topic}")
                    webbrowser.open(f"https://www.google.com/search?q={topic}")
                else:
                    speak("What would you like me to search for?")
            else:
                speak("I am not sure how to help with that yet")
except KeyboardInterrupt:
    print("\nAssistant stopped by user. Goodbye!")
