from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.events'

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    days_plus=0
    date_1=datetime.datetime.today()+datetime.timedelta(days=days_plus)
    #time_1=datetime.time()+datetime.timedelta(days=days_plus)
    d1=date_1
    d2=(date_1+datetime.timedelta(days=0))
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    book_mass=[]
    book_mass_id=[]
    # Call the Calendar API
    now = d2#+ 'Z' # 'Z' indicates UTC time
    now1= now.isoformat() + 'Z'
    print(now)
    print(now1)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now1,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        book_mass_id.append(event['id'])
        #event["summary"]='утра не будет'
      
        #created_event = service.events().update(calendarId='primary',eventId=event['id'],body=event).execute()
        
        if 'summary' in event:
            print(start, event['summary'])
            book_mass.append(event['summary'])
        else:
            print(",tp pfujkjdrf")
            book_mass.append('пусто')

    
    print(book_mass)
    print(book_mass_id)
if __name__ == '__main__':
    main()
