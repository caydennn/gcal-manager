from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def getService():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def getAllEvents(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    print ("Getting all events...")
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    
    events = events_result.get('items', [])
    print (f'{len(events)} item in total')
    return events


"""
Args: Events[] , Keywords[]
Returns: List of Event Ids
Function that takes in list of events and keywords and checks which events contain those keywords.
It then returns the list of event ids
"""
def parseEvents( events, keywords):
    id_list = []
    # Check the list of events for keywords and get the IDS
    for event in events:
        for keyword in keywords:
            if keyword in event['summary']:
                print (f"Found event with matching keyword: ({event['summary']} , {keyword})")
                id_list.append(event['id'])

                break

    print (f"Number of events with keywords found: {len(id_list)}")
    return id_list

def deleteEvent(service, event_id):
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    print (f"Deleting event: {event['summary']}")

    service.events().delete(calendarId='primary', eventId=event_id).execute()
    return

def testDeleteEvent(service):
    event_id = '785grn7j0ub7skh9dqk9gqvnb2'
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    print (f"Deleting event: {event['summary']}")
    service.events().delete(calendarId='primary', eventId=event_id).execute()
   
    return 


if __name__ == '__main__':
    keywords = []

    service = getService()
    events = getAllEvents(service)
    event_ids = parseEvents(events, keywords )
    verification = input("Proceed with delete? y/n")

    if verification == 'y':
        for event_id in event_ids:
            deleteEvent(service, event_id)

        print ("Done!") 
    else:
        print ("Process cancelled.")