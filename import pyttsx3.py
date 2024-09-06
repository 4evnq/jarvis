import pyttsx3
from transformers import pipeline
import speech_recognition as sr

# Инициализация TTS
engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 150)  # Скорость речи
    engine.setProperty('volume', 1)   # Громкость речи
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите что-нибудь...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {text}")  # Убедитесь, что здесь выводится корректный текст
            return text
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания")
            return None


# Инициализация модели для генерации текста
generator = pipeline('text-generation', model='gpt2')

def chat_with_ai(text):
    response = generator(text, max_length=50, num_return_sequences=1, temperature=0.7, top_k=50)
    return response[0]['generated_text']


def main():
    while True:
        text = listen()
        if text:
            if "пока" in text.lower():
                speak("До свидания!")
                break
            response = chat_with_ai(text)
            print(f"AI: {response}")
            speak(response)

if __name__ == "__main__":
    main()
