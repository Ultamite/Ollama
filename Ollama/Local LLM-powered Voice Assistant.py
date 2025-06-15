import speech_recognition as sr
import whisper
import ollama
import pyttsx3
import tempfile
import os

# Initialize components
recognizer = sr.Recognizer()
model = whisper.load_model("base")  # You can change to "tiny", "small", etc.
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def record_audio():
    print("Listening... Speak into the mic.")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    print("Recording complete.")
    
    # Save to temp WAV file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        temp_filename = f.name
        with open(temp_filename, "wb") as file:
            file.write(audio.get_wav_data())
    return temp_filename

def transcribe_audio(audio_path):
    print("Transcribing...")
    result = model.transcribe(audio_path)
    return result['text']

def ask_llm(prompt_text):
    print("Querying LLM...")
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt_text}]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        return f"Error: {e}"

def speak(text):
    print("Speaking response...")
    engine.say(text)
    engine.runAndWait()

def main():
    try:
        audio_path = record_audio()
        transcribed_text = transcribe_audio(audio_path)
        print(f"You said: {transcribed_text}")

        response = ask_llm(transcribed_text)
        print(f"AI: {response}")

        speak(response)

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    while True:
        input("Press Enter to ask a question (Ctrl+C to quit)...")
        main()
