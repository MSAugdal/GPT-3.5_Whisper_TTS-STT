import speech_recognition as sr
import openai
from playsound import playsound
from gtts import gTTS
from time import sleep
from termcolor import colored
import sys
# pip install SpeechRecognition
# pip install PyAudio
# pip install pyobjc
# pip install gTTS
# pip install playsound
# pip install openai
# pip install termcolor


class STT_TTS:
    def __init__(self, api_key):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 2
        openai.api_key = api_key

    def speechToPrompt(self):
        try:
            with sr.Microphone(device_index=self.showDevices()) as source:
                print(colored("\nGPT-3 is now listening...", 'yellow'))
                try:
                    audio = self.recognizer.listen(source, timeout=6)
                except:
                    print(colored("\nNo speech detected", 'red'))
                    print(colored("If you did speak, please run program again and choose a different device...", 'red'))
                    sys.exit()
                print(colored("\nProcessing...", 'yellow'))
                with open("microphone-results.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                audio = open("microphone-results.wav", "rb")
                with open("microphone-results.wav", "rb") as f:
                    text = openai.Audio.transcribe("whisper-1", f)
                    return dict(text)["text"]
        except:
            print(colored("\nMicrophone not working", 'red'))
            print(colored("Please run program again and choose a different device...", 'red'))
            sys.exit()

    def promptToGPT(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            temperature=0.5,
            max_tokens=100,
            messages=[
                {"role": "system", "content": "you are chatGPT-3"},
                {"role": "user", "content": prompt},
            ],
        )
        return response["choices"][0]["message"]["content"]

    def gptResponseToTTS(self, GPT_response):
        tts = gTTS(text=GPT_response, lang="en")
        tts.save("response.mp3")
        playsound("response.mp3")

    def showDevices(self):
        devices = {k: v for k, v in enumerate(sr.Microphone.list_microphone_names())}
        for k, v in devices.items():
            print(f"{k}: {v}")
        choice = int(input(colored("Enter device index: ", 'yellow')))
        if choice in devices:
            return choice
        print("Invalid choice")
        sleep(1)
        print("\033c")
        self.showDevices()
        return

    def run(self):
        print("\033c")
        print(f"{colored('Welcome to GPT-3!', 'yellow')}\nIt knows many languages, but {colored('it speaks (TTS) english best.', 'yellow')}\n\n{colored('Please choose a device to use as microphone: ','yellow')}")
        prompt = self.speechToPrompt()
        if prompt:
            print(f"\n{colored('Prompt:', 'blue')} {prompt}")
            response = self.promptToGPT(prompt)
            print(f"\n{colored('Response:','green')} {response}")
            self.gptResponseToTTS(response)


STT_TTS("API_KEY").run()
