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
        self.chosenDevice = None
        self.messages = [{"role": "system", "content": "you are assistant"}]

    def speechToPrompt(self):
        try:
            with sr.Microphone(device_index=self.chosenDevice) as source:
                print(colored("\nGPT-3 is now listening...", 'yellow'))
                audio = self.recognizer.listen(source, timeout=4)
                print(colored("\nProcessing...", 'yellow'))
                with open("microphone-results.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                audio = open("microphone-results.wav", "rb")
                with open("microphone-results.wav", "rb") as f:
                    text = openai.Audio.transcribe("whisper-1", f)
                    return dict(text)["text"]
        except:
            print(colored("\nEither microphone doesn't work or you didn't speak", 'red'))
            print(colored("Please run program again and choose a different device...", 'red'))
            sys.exit()

    def promptToGPT(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0301",
            temperature=0.5,
            max_tokens=100,
            messages=self.messages
        )
        self.messages.append({"role": response["choices"][0]["message"]["role"],
                              "content": response["choices"][0]["message"]["content"]})
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
            self.chosenDevice = choice
            return choice
        print("Invalid choice")
        sleep(1)
        print("\033c")
        self.showDevices()
        return

    def continuePrompt(self):
        choice = input(colored("Would you like to continue? (y/n): ", 'yellow'))
        if choice == "y":
            self.getAndShowPrompt()
        elif choice == "n":
            print(colored("Goodbye!", 'yellow'))
            sys.exit()
        else:
            print(colored("Invalid choice", 'red'))
            sleep(1)
            self.continuePrompt()

    def getAndShowPrompt(self):
        prompt = self.speechToPrompt()
        print(f"\n{colored('Prompt:', 'blue')} {prompt}")
        response = self.promptToGPT(prompt)
        print(f"\n{colored('Response:','green')} {response}")
        self.gptResponseToTTS(response)
        self.continuePrompt()

    def run(self):
        print("\033c")
        print(f"{colored('Welcome to GPT-3!', 'yellow')}\nIt knows many languages, but {colored('it speaks (TTS) english best.', 'yellow')}\n\n{colored('Please choose a device to use as microphone: ','yellow')}")
        self.showDevices()
        self.getAndShowPrompt()


STT_TTS("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").run()
