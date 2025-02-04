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

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def search_messages(service, query, label_id="", max_results=5):
    """
    Search for messages in the user's Gmail account based on a query.
    Limit the number of messages fetched using max_results.
    """
    if label_id != "":
        result = service.users().messages().list(userId='me', q=query, labelIds=label_id, maxResults=max_results).execute()
    else:
        result = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
    
    messages = result.get('messages', [])
    return messages

def build_query(sender=None, before=None, after=None, label=None):
    """
    Build a query string for Gmail API based on sender, before date, and after date.
    """
    query = []
    if sender:
        query.append(f"from:{sender}")
    if before:
        query.append(f"before:{before}")
    if after:
        query.append(f"after:{after}")
    if label:
        query.append(f"label:{label}")
    
    if not query:
        return ""
     
    return " ".join(query)

# utility functions
def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def parse_parts(service, parts, message):
    """
    Utility function that parses the content of an email partition.
    Returns the plain text and HTML content, and attachments metadata.
    """
    email_content = {
        "text": "",
        "html": "",
        "attachments": []
    }

    if parts:
        for part in parts:
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            filename = part.get("filename")

            if part.get("parts"):
                # Recursively parse nested parts
                nested_content = parse_parts(service, part.get("parts"), message)
                email_content["text"] += nested_content["text"]
                email_content["html"] += nested_content["html"]
                email_content["attachments"].extend(nested_content["attachments"])

            if mimeType == "text/plain" and data:
                email_content["text"] += urlsafe_b64decode(data).decode()
            elif mimeType == "text/html" and data:
                email_content["html"] += urlsafe_b64decode(data).decode()
            elif "attachmentId" in body:
                # Handle attachments
                attachment_id = body.get("attachmentId")
                email_content["attachments"].append({
                    "filename": filename,
                    "size": file_size,
                    "attachment_id": attachment_id
                })

    return email_content

def read_message(service, message):
    """
    Reads an email's details and returns structured data.
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")

    email_data = {
        "id": message["id"],
        "from": "",
        "to": "",
        "subject": "",
        "date": "",
        "text": "",
        "html": "",
        "attachments": []
    }

    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == "from":
                email_data["from"] = value
            elif name.lower() == "to":
                email_data["to"] = value
            elif name.lower() == "subject":
                email_data["subject"] = value
            elif name.lower() == "date":
                email_data["date"] = value

    if parts:
        content = parse_parts(service, parts, message)
        email_data["text"] = content["text"]
        email_data["html"] = content["html"]
        email_data["attachments"] = content["attachments"]

    return email_data


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)