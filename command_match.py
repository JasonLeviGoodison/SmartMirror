import json
import requests
import base64
import urllib
from intent_types import *;

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

def getIntentFromResponse(intent):
    intents = Intents()
    if (intent == "greetings"):
        return intents.GREETINGS
    elif (intent == "weather"):
        return intents.WEATHER
    elif (intent == 'get-calendar'):
        return intents.GET_CALENDAR
    elif (intent == 'set-calendar'):
        return intents.SET_CALENDAR
    elif (intent == 'play-music'):
        return intents.PLAY_MUSIC
    elif (intent == 'stop'):
        return intents.STOP
    else:
        return -1

#intentTypes = Intents();
class CommandMatch:
    @staticmethod
    def getIntent(command):
        witResponse = json.loads(sendMessageToWit(command));
        print(witResponse[u'entities'])
        if (witResponse[u'entities'] and witResponse[u'entities'][u'intent']):
            #return witResponse.intent.value;
            witIntent =  witResponse[u'entities'][u'intent'][0][u'value'];
            print("intent: ", witIntent)
            intent = getIntentFromResponse(witIntent)
            print(intent)
            return intent;
        return -1;