import json
import requests
import base64
import urllib
from intent_types import *;
import datetime
intents = Intents()

with open ("apikey.txt", "r") as myfile:
    apiKey=myfile.read().replace('\n','')

def sendMessageToWit(message):
    global apiKey
    urlEncodedMessage = urllib.urlencode({'message': message})[8:];
    print('url encoded thing', urlEncodedMessage)
    url = 'https://api.wit.ai/message?v=20180515&q=' + urlEncodedMessage;
    headers = {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json'
    };
    r = requests.post(url=url, data=json.dumps({}), headers=headers);
    return r.content

def getIntentFromResponse(intent, params = {}):
    if (intent == "greetings"):
        return intents.GREETINGS, None
    elif (intent == "weather"):
        return intents.WEATHER, None
    elif (intent == 'get-calendar'):
        try:
            return intents.GET_CALENDAR_DAY, params[u'datetime'][0][u'value']
        except KeyError:
            return intents.GET_CALENDAR, None
    elif (intent == 'set-calendar'):
        return prepareSetCalendar(params)
    elif (intent == 'play-music'):
        return intents.PLAY_MUSIC, None
    elif (intent == 'stop'):
        return intents.STOP, None
    else:
        return -1

#intentTypes = Intents();
def prepareSetCalendar(params):
    value = params[u'reminder'][0][u'value']
    try:
        day = params[u'datetime'][0][u'value']
        return intents.SET_CALENDAR, [day, value]
    except KeyError:
        day = unicode(datetime.date.today()) + 'T'
        return intents.SET_CALENDAR, [day, value]

class CommandMatch:
    @staticmethod
    def getIntent(command):
        witResponse = json.loads(sendMessageToWit(command));
        witResponse = witResponse[u'entities']
        if (u'intent' in witResponse):
            witIntent =  witResponse[u'intent'][0][u'value'];
            intent, params = getIntentFromResponse(witIntent, witResponse)
            return intent, params
        if (u'reminder' in witResponse):
            return prepareSetCalendar(witResponse)

        return -1;
