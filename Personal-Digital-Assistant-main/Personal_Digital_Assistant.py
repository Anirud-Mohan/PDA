import googletrans
import speech_recognition as sr
import gtts
import playsound
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
from bs4 import BeautifulSoup
import requests
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

recognizer = sr.Recognizer()
microphone=sr.Microphone()

def image_download():
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    microphone=sr.Microphone()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak('whose images should I download for you sir')
        speak('Speak Now')
        print('speak')
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source)
        print(voice)
        print('Recognizing your voice')
        text = recognizer.recognize_google(voice, language='en')
        print('Wait....')
        print(text)
        speak('downloading images for'+text)
        pywhatkit.playonyt(text)
    n_images=50
    img_format = 'png'
    folder_name = text
    def scrappi(data, n_images, img_format, folder_name):
            
        #URL = ['https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q=']
        URL = ['https://www.google.com/search?tbm=isch&q=']
        
        def check(folder_name):
            try: 
                os.mkdir(folder_name)
                return folder_name
            except:
                print("Folder Exist with that name!")
                folder_name = input("Enter a new Folder name: \n")
                try: 
                    os.mkdir(folder_name)
                    return folder_name
                except: return check(folder_name)
                
        folder_name = check(folder_name)

        print('Starting to Download...')

        for i in URL:
            searchurl = i + str(data)
            response = requests.get(searchurl, headers = usr_agent)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            results = soup.findAll('img', limit = n_images + 1)

            if len(results) != 0:
                for i, image in enumerate(results):
                    try: image_link = image["data-srcset"]
                    except:
                        try: image_link = image["data-src"]
                        except:
                            try: image_link = image["data-fallback-src"]
                            except:
                                try: image_link = image["src"]
                                except: pass
                        try:
                            r = requests.get(image_link).content
                            try: r = str(r, 'utf-8')
                            except UnicodeDecodeError:
                                with open(f"{folder_name}/images{i}.{img_format}", "wb+") as f: f.write(r)
                        except: pass
                        
        return 'Successfully Downloaded ' + str(n_images) + ' images'
    scrappi(text,n_images,img_format,folder_name)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def song():
    microphone=sr.Microphone()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak('which song will you like me to play for you')
        speak('Speak Now')
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source)
        print(voice)
        print('Recognizing your voice')
        text = recognizer.recognize_google(voice, language='en')
        print('Wait....')
        print(text)
        speak('playing song'+text)
        pywhatkit.playonyt(text)

def tellDay():
    day = datetime.datetime.today().weekday() + 1

    Day_dict = {1: 'Monday', 2: 'Tuesday', 
                3: 'Wednesday', 4: 'Thursday', 
                5: 'Friday', 6: 'Saturday',
                7: 'Sunday'}
        
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
        speak("The day is " + day_of_the_week) 

def translation():
    microphone=sr.Microphone()
    recognizer = sr.Recognizer()
    translator = googletrans.Translator()
    input_lang = 'en'
    output_lang = 'hi'
    with sr.Microphone() as source:
        print('Speak Now')
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source)
        print(voice)
        print('Recognizing your voice')
        text = recognizer.recognize_google(voice, language=input_lang)
        print('Wait....')
        print(text)
        print('translating...')

    translated = translator.translate(text, dest=output_lang)
    print(translated.text)
    converted_audio = gtts.gTTS(translated.text, lang=output_lang)
    print('saving audio')
    converted_audio.save('translate.mp3')
    print('playing audio')
    playsound.playsound('translate.mp3')

def start():
    microphone=sr.Microphone()
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Speak Now')
        speak('speak')
        recognizer.adjust_for_ambient_noise(source)
        voice = recognizer.listen(source)
        print(voice)
        print('Recognizing your voice')
        
        try:
            text = recognizer.recognize_google(voice, language='en')
            if (text==str('translate')):
                translation()
                start()
            elif (text==str('how are you')):
                speak("I am fine")
                start()
            #elif (text==str('What is your Name') or text==str('Your Name') or text==str('name')):
            elif 'your name' in text:
                speak('My Name is KAKATONA')
                start()
            elif (text==str('Quit') or text==str('turn off') or text==str('thank you') or text==str('exit')):
                speak('Thank You Sir')
                speak('Call me whenever u need my help')
            elif (text==str('search')):
                speak('okay')
            elif (text==str('play song')):
                song()
                start()
            elif 'time' in text:
                time = datetime.datetime.now().strftime('%I: %M')
                print(time)
                speak('current time is' + time)
                start()
            elif 'tell me about' in text or 'about' in text:
                thing = text.replace('tell me about', '')
                info = wikipedia.summary(thing, 2)
                print(info)
                speak(info)
                start()
            elif 'who are you' in text:
                speak('I am your personal Assistant KAKATONA')
                start()
            elif 'what can you do for me' in text:
                speak('I can play songs, tell time, and help you go with wikipedia')
                start()
            elif 'which day it is' in text:
                tellDay()
                start()
            #elif 'image' in text or 'images' in text:
                #webbrowser.open('https://www.google.com/search?tbm=isch&q=' + str(text))
                #start()
            elif 'video' in text or 'videos' in text:
                webbrowser.open('https://www.google.com/search?tbm=vid&q=' + str(text))
                start()
            elif 'news' in text:
                webbrowser.open('https://www.google.com/search?tbm=nws&q=' + str(text))
                start()
            elif 'download image' in text:
                image_download()
                start()
            else: 
                print(text)
                speak('searching'+text)
                if text == 'download image':
                    image_download()
                else:
                    pywhatkit.search(text)
                start()

        except Exception as e:
            speak("Speech not recognised")
            start()
speak('My name is KAKATONA')
start()
