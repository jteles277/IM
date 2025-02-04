import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os 
 
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type 


def classify_email(service, message_id, label_name):
        """
        Classify the email by applying a label.
        """

        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name']+ " "+label['id'])
        # Get the label ID, create it if it doesn't exist
        #label_id = self.get_or_create_label(label_name)
        print("label_name: "+label_name)
        label_id = label_name

        # Apply the label to the email
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': [label_id]}
        ).execute()

def archive_email(service, message_id):
    """
    Archives an email by removing it from the INBOX label.
    """
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['INBOX']}
    ).execute()

def delete_email(service, message_id):
    """
    Moves an email to the trash.
    """
    service.users().messages().delete(
        userId='me',
        id=message_id
    ).execute()