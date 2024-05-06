import sounddevice as sd
import soundfile as sf
import warnings, time, os
import threading
import time
import pyautogui
import webbrowser
from faster_whisper import WhisperModel # import faster whisper model as according to their GitHub, it is around 4x faster than the original whisper model
from openai import OpenAI               # and uses less than half the memory (both vram and ram)
from pathlib import Path
import speech_recognition as sr


# Setup environment
warnings.filterwarnings("ignore", category=DeprecationWarning)
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Configuration constants
wake_word = "nova" # Wake word to activate the assistant
should_run = True # Flag to control the main loop
source = sr.Microphone() # Microphone source for speech recognition
recognizer = sr.Recognizer() # Speech recognizer
model_size = "medium.en" # Model size for the Whisper Model
whisper_model = WhisperModel(model_size, device="cuda", compute_type="float16") # Whisper Model for speech transcription
#whisper_model = WhisperModel(model_size, device="cpu", compute_type="float32") # use cpu and float32 (cpu does not support fp16)
client = OpenAI(api_key="YOUR_API_KEY") # OpenAI API client and api key

# Initialize messaging for OpenAI
messages = [{"role": "system", "content": "You are my best friend. We have the funniest 'mean' banter."}]

# Audio playback control flag
stop_audio = False

def play_audio(audio_data, sample_rate):
    global stop_audio
    sd.play(audio_data, sample_rate)
    while not stop_audio and sd.get_stream().active:
        sd.sleep(100)
    sd.stop()

# Generate audio from text using OpenAI API and play it back using sounddevice library
def generate_audio(prompt):
    global stop_audio
    stop_audio = False
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=prompt
    )
    response.stream_to_file(speech_file_path)
    audio_data, sample_rate = sf.read(speech_file_path)
    
    # Create a thread for audio playback
    audio_thread = threading.Thread(target=play_audio, args=(audio_data, sample_rate))
    audio_thread.start()

# Generate text using OpenAI API and print it to the console and call generate audio function to read the generated text
def generate_text(command):
    messages.append({"role": "user", "content": command})
    response_start_time = time.time()  # Start timing

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )

    response_time = time.time() - response_start_time  # End timing and calculate duration
    print(f"Response Generation Time: {response_time} seconds")  # Display the response generation time

    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": bot_response})
    print(bot_response)
    generate_audio(bot_response)


# Listen for the wake word and transcribe the command using the Whisper Model
def listening():
    with source as s:
        print("Listening for wake word...")
        recognizer.adjust_for_ambient_noise(s)
        audio = recognizer.listen(s)

    transcription_start_time = time.time()  # Start timing

    try:
        with open("command.wav", "wb") as f: # Open a file to write the audio data to
            f.write(audio.get_wav_data()) # Save the audio data to a file

        segments, info = whisper_model.transcribe("command.wav", beam_size=5) # Transcribe the audio using the Whisper Model
        transcription_time = time.time() - transcription_start_time  # End timing and calculate duration
        print(f"Transcription Time: {transcription_time} seconds")  # Display the transcription time

        prompt = " ".join(segment.text for segment in segments).lower().strip() # Combine the segments into a single string
        print("You:", prompt) # Print the transcribed command

        if prompt.startswith(wake_word.lower()): # Check if the wake word is detected
            command = prompt[len(wake_word):].strip() # Extract the command after the wake word
            if "open youtube" in command: # Check if the command is to open YouTube
                generate_audio("Opening YouTube.") 
                webbrowser.open("https://www.youtube.com/") # Open YouTube in the default web browser
                return  # Stop further processing after handling the command
            elif "take a screenshot" in command:
                pyautogui.screenshot("screenshot.png") # Take a screenshot and save it as "screenshot.png"
                generate_audio("I took a screenshot for you.") 
                return  # Stop further processing after handling the command
            elif "open discord" in command: 
                generate_audio("Opening Discord.") 
                pyautogui.hotkey('win')
                pyautogui.typewrite('discord')
                pyautogui.press('enter')
                return
            elif "open steam" in command:
                generate_audio("Opening Steam.")
                pyautogui.hotkey('win')
                pyautogui.typewrite('steam')
                pyautogui.press('enter')
                return
            elif "open league" in command:
                generate_audio("Opening League of Legends.")
                pyautogui.hotkey('win')
                pyautogui.typewrite('league')
                pyautogui.press('enter')
                return
            elif "open runescape" in command:
                generate_audio("Opening Runescape.")
                pyautogui.hotkey('win')
                pyautogui.typewrite('jagex')
                pyautogui.press('enter')
                return
            else:
                return command  # Send other commands for ChatGPT processing
        else:
            print("Wake word not detected. Please start with 'nova'.")
            return None
    except sr.UnknownValueError:
        print("Sorry, I didn't quite catch that.")
        return None
    except sr.RequestError as e:
        print(f"Unable to receive audio. Error: {str(e)}")
        return None



# Key listener function to stop audio playback on Enter key press
def key_listener():
    global stop_audio
    input("Press Enter to stop audio...\n")
    stop_audio = True

def main():
    # Start the key listener thread
    listener_thread = threading.Thread(target=key_listener)
    listener_thread.start()

    while should_run:
        command = listening()
        if command:
            generate_text(command)
        time.sleep(1)
        
    listener_thread.join() # Wait for the key listener thread to finish

if __name__ == "__main__":
    main()
