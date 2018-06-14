from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

class CalendarAPI:
    @staticmethod
    def getNextWeek():
        page_token = None
        while True:
            timeDelta = datetime.timedelta(weeks=1)
            today = datetime.date.today()
            events = service.events().list(
                calendarId='primary', 
                pageToken=page_token, 
                timeMin=str(today) + 'T10:00:00-07:00',
                timeMax=str(today + timeDelta) + 'T10:00:00-07:00'
                ).execute();
            for event in events['items']:
                print(event['summary'])
            page_token = events.get('nextPageToken')
            if not page_token:
                break
    @staticmethod
    def getToday():
        allEvents = []
        page_token = None
        while True:
            timeDelta = datetime.timedelta(days=1)
            today = datetime.date.today()
            events = service.events().list(
                calendarId='primary', 
                pageToken=page_token, 
                timeMin=str(today) + 'T10:00:00-07:00',
                timeMax=str(today + timeDelta) + 'T10:00:00-07:00'
                ).execute();
            for event in events['items']:
                allEvents += [event]
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        return allEvents