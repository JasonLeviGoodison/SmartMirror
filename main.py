from gtts import *;
import speech_recognition as sr;
import re;
import os;
from response_strings import ResponseStrings;
from command_match import CommandMatch;
from intent_types import *;
from weather import WeatherIntent;
from calendar_api import CalendarAPI;
intents = Intents();
responseStrings = ResponseStrings();
launchPhrase = 'hey Jarvis'

def respond(sentence):
    tts = gTTS(text=sentence, lang='en-us');
    tts.save('assets/sentence.mp3');
    os.system('mpg123 assets/sentence.mp3');

def listening():
    os.system('mpg123 assets/listening.mp3');

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
    #Continually listen for a command
    while True:
        command = listenForCommand();
        if launchPhrase == command:
            listening();
            command = listenForCommand();
            dealWithCommand(command);

def dealWithCommand(command):
    if (command == 'timeout'):
        respond(responseStrings.timeout)
        return;
    if (command == 'update yourself'):
        respond("About to update")
        update();

    commandIntent, params = CommandMatch.getIntent(command);

    if commandIntent == intents.GREETINGS:
        respond(responseStrings.nothing_much_you);
    elif commandIntent == intents.WEATHER:
        respond(weatherCommand());
    #elif commandIntent == intents.WHO_MADE_YOU:
    #    respond(responseStrings.creator);
    elif commandIntent == intents.GET_CALENDAR or commandIntent == intents.GET_CALENDAR_DAY:
        if (params != None):
            respond(calendarCommand(params[:params.index('T')]));
        else:
            respond(calendarCommand(None))
    elif commandIntent == intents.SET_CALENDAR:
        CalendarAPI.setCalendarEvent({'summary': params[1], 'datetime': params[0][:params[0].index('T')]})
        respond(responseStrings.set_calendar)
    elif commandIntent == intents.PLAY_MUSIC:
        respond("i'll play some music");
    elif commandIntent == intents.STOP:
        respond(responseStrings.stop)
    else:
        respond(responseStrings.cant_help);

def update():
    os.system("update/update.sh");
    return "Updated"

#use the weather api to return the weather for the location
def weatherCommand():
    weather = WeatherIntent.getWeather()
    respond = "Right now, the weather is " + weather['weather'] + \
        " and the temperature is " + str(int(weather['temp'])) + " degrees celsius" + \
        " in " + weather['city']
    return respond

#use the calendar api to return todays calendar
def calendarCommand(date):
    respond = "You have ";
    events = []
    if (date != None):
        events = CalendarAPI.getDay(date)
    else:
        events = CalendarAPI.getToday()
    if (events == []):
        events = [{'summary': "nothing planned"}]
    for i, event in enumerate(events):
        if (i == 0):
            respond += event['summary']
        else:
            respond += ' and ' + event['summary']
    return respond + ' on your calendar'

#use the google calendar api to set an event on day
def setCalendar(day = "today", event = "event"):
    return responseStrings.set_calendar;

#listenForInitCommand()
update()