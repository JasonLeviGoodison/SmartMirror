from gtts import *;
import speech_recognition as sr;
import re;
import os;
from response_strings import ResponseStrings;
from command_match import CommandMatch;
from intent_types import *;
from weather import WeatherIntent;

responseStrings = ResponseStrings();
launchPhrase = 'hey Jarvis'

'''feature ideas:
    Google calendar integration: display any events for the day
    not listening anymore sound
'''

def respond(sentence):
    tts = gTTS(text=sentence, lang='en-us');
    tts.save('sentence.mp3');
    os.system('mpg123 sentence.mp3');
    #TODO see if removing is a good idea
    os.system('rm sentence.mp3');

def listening():
    os.system('mpg123 listening.mp3');

def listenForCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("ready for command");
        r.pause_threshold = 1;
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source);
        
        try:
            command = r.recognize_google(audio);
            print ("I heard: " + command);
            return command;
        except Exception:
            return 'timeout'

def listenForInitCommand():
    skip_hello = False;
    #Continually listen for a command
    while True:
        command = listenForCommand();
        if launchPhrase == command:
            #if skip_hello is False:
            listening();
            command = listenForCommand();
            dealWithCommand(command);


#harcoded commands for now, in future looking for an ML model
# that can determine closest command (knn?)
def dealWithCommand(command):
    print(command, "!!")
    if (command == 'timeout'):
        respond(responseStrings.timeout)
        return;
    intents = Intents();
    commandIntent = CommandMatch.getIntent(command);
    
    if commandIntent == intents.GREETINGS:
        respond(responseStrings.nothing_much_you);
    elif commandIntent == intents.WEATHER:
        respond(weatherCommand());
    #elif commandIntent == intents.WHO_MADE_YOU:
    #    respond(responseStrings.creator);
    elif commandIntent == intents.GET_CALENDAR:
        respond("i'll get you calendar");
    elif commandIntent == intents.SET_CALENDAR:
        respond("i'll add that to your calendar");
    elif commandIntent == intents.PLAY_MUSIC:
        respond("i'll play some music");
    elif commandIntent == intents.STOP:
        respond(responseStrings.stop)
    else:
        respond(responseStrings.cant_help);

#use the weather api to return the weather for the location
def weatherCommand():
    weather = WeatherIntent.getWeather()
    respond = "Right now, the weather is " + weather['weather'] + \
        " and the temperature is " + str(int(weather['temp'])) + " degrees celsius"
    return respond
#use the google calendar api to get the days stuff on it
def getCalendar():
    return "Meeting with Alex"

#use the google calendar api to set an event on day
def setCalendar(day = "today", event = "event"):
    return responseStrings.set_calendar;

#TODO Add in some temps and API calls
def getWeatherIn(location):
    weather = 'sunny'
    return responseStrings.weather_is_begin + weather + responseStrings.weather_is_end + location;

listenForInitCommand()
#dealWithCommand("Whats the weather like")