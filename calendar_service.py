import os.path
from datetime import datetime, timedelta, timezone

# Google Authentication Libraries
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# We use the Calendar scope this time!
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """Authenticates and returns the Calendar service object."""
    creds = None
    
    # 1. Use 'calendar_token.json' (so it doesn't overwrite your gmail token!)
    # Check if 'calendar_token.json' exists. If yes, load it.
    if os.path.exists('calendar_token.json'):
        creds = Credentials.from_authorized_user_file('calender_token.json',SCOPES)

    # 2. If no valid creds, handle the login flow using 'credentials.json'
    # Save the new creds to 'calendar_token.json'
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
            creds = flow.run_local_server(port=0)
        with open('calender_token.json','w') as token:
            token.write(creds.to_json())
        
    # 3. Build the service and return it
    # Note: Calendar uses 'calendar' and 'v3'
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def fetch_todays_schedule():
    """Fetches today's meetings and returns them as a single string."""
    service = get_calendar_service()
    if not service:
        return None

    # 1. Calculate the start and end of TODAY in the format Google wants (RFC3339)
    # I have provided this tricky time math for you:
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0).isoformat()
    end_of_day = now.replace(hour=23, minute=59, second=59).isoformat()

    # 2. Call the Calendar API to get today's events
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=start_of_day,
        timeMax=end_of_day, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    # 3. Create an empty string to hold the schedule text
    all_calender_text = ""
    
    # 4. If 'events' is empty, return a string saying "No meetings today!"
    if not events:
        return "No meetings today!"

    # 5. Loop through the events
    #    - Get the event name: event['summary']
    #    - Get the start time: event['start'].get('dateTime', event['start'].get('date'))
    #    - Append them to your string variable
    for event in events:
        event_name = event['summary']
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        all_calender_text += f"Event Name:{event_name}\n Starting Time:{start_time}\n......\n"

    # 6. Return the giant string of today's schedule!
    return all_calender_text