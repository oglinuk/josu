'''
JOSU
    * Open-source personal virtual assistant
    * Default commands
        * commands
        * what time is it
        * where is
        * play
        * quit
        * sleep
'''
import sys
import time
import csv
import subprocess
import speech_recognition as sr
from gtts import gTTS
from time import ctime
from mutagen.mp3 import MP3

class JosuVA(object):
    def __init__(self):
        self.commandDictPath = 'josuCommands.csv'
        self.commandDict = {}
        self.data = None
        self.loadCommandDict()

    # core method - entry point for the Josu virtual assistant
    def josu(self):
        while True:
            print('zzz...')
            self.data = self.recordVoiceInput()
            if 'assistant' in self.data:
                self.responseOutput('What can I do for you?')
                while self.data != 'sleep':
                    self.data = self.recordVoiceInput()
                    self.askJosu()

    # core method - iterates through command dictionary to see if a key matches with current self.data, if a key is found it responds with tts accoring to the matching value
    def askJosu(self):
        for key in self.commandDict.keys():
            if key in self.data:
                self.responseOutput(eval(self.commandDict[key]))

    # core method - text to speech response method based on value from command dictionary
    def responseOutput(self, prVoiceInput):
        print(prVoiceInput)
        tts = gTTS(text=str(prVoiceInput), lang='en')
        tts.save('audio.mp3')
        # this will need to be changed to your installed media player with the correct path
        subprocess.call([r'C:\Users\Steve\Desktop\Desktop\MPC-HC.1.7.10.x64\mpc-hc64.exe', 'audio.mp3'])
        time.sleep(MP3('audio.mp3').info.length)
        print('Ask command now')

    # core method - records voice command input and returns the recorded input
    def recordVoiceInput(self):
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            audio = rec.listen(source)
        try:
            self.data = rec.recognize_google(audio)
            print('{}'.format(self.data))
        except sr.UnknownValueError:
            if self.data == None or self.data == '' or self.data == 'sleep':
                pass
            else:
                print('Google Speech Recognition could not understand that audio')
                self.responseOutput('Sorry, that command is not recognized')
        except sr.RequestError:
            print('Could not request results from Google Speech Recognition service')

        return self.data

    # loads a pre-existing command dictionary
    def loadCommandDict(self):
        print('Loading command dictionary...')
        for row in csv.reader(open(r'{}'.format(self.commandDictPath))):
            key, value = row
            self.commandDict[key] = value
        print('Successfully loaded command dictionary...')

    # command method - commands - lists off all available commands
    def getCommands(self):
        self.responseOutput([keys for keys in self.commandDict.keys()])

    # command method - what time is it - tells the current datetime
    def getTime(self):
        self.responseOutput(ctime())

    # command method - where is - opens Google maps displaying the specified location
    def whereIs(self):
        data = str(self.data).split(' ')
        print(data)
        location = data[2]
        self.responseOutput('Hold on, let me load Google maps to show you where {} is'.format(location))
        # this will need to be changed to your installed web browser with the correct path
        subprocess.call([r'C:\Program Files\Mozilla Firefox\firefox.exe', 'https://www.google.nl/maps/place/{}'.format(location)])

    # command method - play - opens Youtube and displays results for specified song
    def playSong(self):
        data = str(self.data).split(' ')
        song = data[2]
        self.responseOutput('Playing {}'.format(song))
        # this will need to be changed to your installed web browser with the correct path
        subprocess.call([r'C:\Program Files\Mozilla Firefox\firefox.exe', 'https://www.youtube.com/results?search_query={}'.format(song)])

    # command method - quit - exits the program
    def quitJosu(self):
        self.responseOutput('Thank you for using Josu, closing now...')
        sys.exit()

def main():
    va = JosuVA()
    va.josu()

if __name__ == '__main__':
    main()
