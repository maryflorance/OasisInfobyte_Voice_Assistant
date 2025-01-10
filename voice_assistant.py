import speech_recognition as sr  # For recognizing speech
import pyttsx3                  # For text-to-speech functionality
import datetime                 # For fetching date and time
import requests                 # For HTTP requests (e.g., weather API)
import smtplib                  # For sending emails
from transformers import pipeline  # For NLP tasks (e.g., summarization)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Captures and recognizes user voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening...")
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that. Please say it again.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""
        except Exception as e:
            speak(f"An error occurred: {e}")
            return ""

def get_time_date():
    """Fetches current time and date."""
    now = datetime.datetime.now()
    time = now.strftime("%H:%M:%S")
    date = now.strftime("%Y-%m-%d")
    return time, date

def get_weather(city):
    """Fetches weather details for the specified city."""
    api_key = "10253bd215f7b3cbcb5dc960670955ea"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response["cod"] == 200:
            weather = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            return f"The weather in {city} is {weather} with a temperature of {temp}°C."
        else:
            return "I couldn't find the city. Please try again."
    except Exception as e:
        return f"An error occurred while fetching weather: {e}"

def send_email(to_email, subject, body):
    """Sends an email."""
    sender_email = "maryflorance2004@gmail.com"  # Replace with your email
    sender_password = "Abcd123"     # Replace with your app password
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(sender_email, to_email, message)
            speak("Email sent successfully!")
    except Exception as e:
        speak(f"Failed to send email: {e}")

def handle_command(command):
    """Processes user commands and calls appropriate functions."""
    if "time" in command or "date" in command:
        time, date = get_time_date()
        speak(f"The time is {time} and today's date is {date}.")
    elif "weather" in command:
        speak("Which city?")
        city = listen()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
    elif "email" in command:
        speak("Who should I send the email to?")
        to_email = listen()
        speak("What is the subject?")
        subject = listen()
        speak("What should I say?")
        body = listen()
        send_email(to_email, subject, body)
    elif "stop" in command or "exit" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    speak("Hello! I'm your voice assistant. How can I assist you today?")
    while True:
        user_command = listen()
        if user_command:
            handle_command(user_command)
