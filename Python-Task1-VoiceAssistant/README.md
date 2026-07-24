# Python Voice Assistant

A beginner level voice assistant built in Python that listens to spoken commands through the microphone and responds using text to speech. It can greet you, tell the time and date, search the web on request and shut down when asked.

## Features

- Captures voice input using the microphone
- Responds to "hello" with a predefined greeting
- Tells the current time on request
- Tells the current date on request
- Performs a web search on a topic you say and opens it in the browser
- Asks you to repeat if it does not understand what you said
- Speaks every response out loud using text to speech
- Stops running when you say "stop" or "exit"

## Tech Stack

- Python
- speech_recognition (captures and converts voice to text)
- pyttsx3 (converts text to speech)
- datetime (fetches current time and date)
- webbrowser (opens search results in the default browser)

## How It Works

1. The assistant greets you when it starts
2. It listens for a voice command through the microphone
3. Google's speech recognition API converts your voice into text
4. The text is checked against a set of keywords (hello, time, date, search, stop)
5. Based on the keyword found, it performs the matching action and replies out loud
6. It keeps listening in a loop until you say "stop" or "exit"

## Installation

```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

## Usage

```bash
python main.py
```

Once running, speak clearly when you see "Speak NOW" printed in the terminal. Example commands:

- "hello"
- "what is the time"
- "what is the date"
- "search python tutorials"
- "stop"

## Error Handling

If the assistant does not understand what you said, it asks you to repeat instead of crashing. If you do not speak within the listening window, it lets you know and listens again on the next loop.

## Notes

This project was built as part of the Oasis Infobyte internship, Python track.
