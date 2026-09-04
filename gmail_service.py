import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Authenticates the user and returns the Gmail service object."""
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('gmail_token.json'):
        creds = Credentials.from_authorized_user_file('gmail_token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('gmail_token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def fetch_yesterdays_emails():
    """Fetches emails from the last 24 hours and combines them into a single string."""
    # 1. Get the authenticated service
    service = get_gmail_service()
    if not service:
        return None

    print("Fetching emails.........\n")
    results = service.users().messages().list(userId='me', q='newer_than:1d').execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found.')
    else:
        all_emails_text = ""
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            
            # Extract headers (like Subject and From)
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')

            # Get the snippet (preview of the email body)
            snippet = msg['snippet']
            all_emails_text += f"FROM: {sender} \n Subject: {subject}\nPreview: {snippet}\n.......\n"

        return all_emails_text