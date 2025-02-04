import os
from flask import Flask, jsonify, abort
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin 
from flask import request  # Import request to handle query parameters


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 
from gmail.gmail_get import search_messages, read_message, build_query
from gmail.gmail_class import classify_email

from datetime import date, datetime, timedelta

today = date.today()

# Flask setup
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
 

# Database model
class EmailModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"Email(sender={self.sender}, title={self.title}, content={self.content})"

# Gmail API setup
SCOPES = ["https://mail.google.com/"]

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

# Resource fields
resource_fields = {
    'id': fields.Integer,
    'sender': fields.String,
    'title': fields.String,
    'content': fields.String
}

# API endpoints
class Email(Resource):
    @marshal_with(resource_fields)
    def get(self, email_id):
        result = EmailModel.query.filter_by(id=email_id).first()
        if not result:
            abort(404, message="Could not find email with that id")
        return result   

class GetEmails(Resource): 
    def get(self):
        try:
            max_results = int(request.args.get("max_results", 30))
            label = str(request.args.get("label", "INBOX"))

            service = get_gmail_service()
            messages = search_messages(service, "", label, max_results) 
            
            emails = [read_message(service, msg) for msg in messages]  # Process and collect email data
            
            return emails  
        except HttpError as error:
            abort(500, description=f"An error occurred: {error}")

class GetEmailsByTime(Resource): 
    def get(self):
        try:
            max_results = int(request.args.get("max_results", 30))
            label = str(request.args.get("label", "INBOX"))
            service = get_gmail_service() 

            since = str(request.args.get("since", ""))
            until = str(request.args.get("until", ""))
            
            if since == "":
                before = (today + timedelta(days=1)).strftime("%Y/%m/%d")
                after = (today - timedelta(days=0)).strftime("%Y/%m/%d")
            elif since == "today":
                before = (today + timedelta(days=1)).strftime("%Y/%m/%d")
                after = (today - timedelta(days=0)).strftime("%Y/%m/%d")
            elif since == "yesterday":
                before = (today + timedelta(days=0)).strftime("%Y/%m/%d")
                after = (today - timedelta(days=1)).strftime("%Y/%m/%d")
            elif until == "":
                before = (datetime.strptime(since,"%Y/%m/%d") + timedelta(days=1)).strftime("%Y/%m/%d")
                after = since
            else:
                before = (datetime.strptime(until,"%Y/%m/%d") + timedelta(days=1)).strftime("%Y/%m/%d")
                after = since

            print(after)
            query = build_query(before=before, after=after)
            
            messages = search_messages(service, query, label, max_results)  # Fetch emails with an empty query (all emails)
            emails = [read_message(service, msg) for msg in messages]  # Process and collect email data
            return emails  
        except HttpError as error:
            abort(500, description=f"An error occurred: {error}")

class GetEmailsBySender(Resource): 
    def get(self):
        try:
            max_results = int(request.args.get("max_results", 30))
            label = str(request.args.get("label", "INBOX"))
            service = get_gmail_service()
            
            sender = str(request.args.get("sender", "")) 
            
            if sender == "":
                sender = 'online@cortefiel.com'  # Replace with the sender's email
            elif sender == "Agatha":
                sender = 'agathabmizurine@gmail.com'
            elif sender == "Linkedin":
                sender = 'updates-noreply@linkedin.com'
            elif sender == "Inês Cruz":
                sender = 'i.cruz@aratall.com'   
            elif sender == "Professor teste":
                sender = 'professorteste27@gmail.com'    
            else:
                sender = 'online@cortefiel.com'  # Replace with the sender's email

            query = build_query(sender=sender)


            messages = search_messages(service, query, label, max_results)  # Fetch emails with an empty query (all emails)
            emails = [read_message(service, msg) for msg in messages]  # Process and collect email data
            return emails  
        except HttpError as error:
            abort(500, description=f"An error occurred: {error}")

class ClassifyEmail(Resource): 
    def post(self):
        try:
            email_id = str(request.args.get("email_id", ""))
            label_name = str(request.args.get("label_name", "Familia"))
            service = get_gmail_service()
            classify_email(service, email_id, label_name)
            return jsonify({"message": "Email classified successfully"})
        except HttpError as error:
            abort(500, description=f"An error occurred: {error}")

# Add resources
api.add_resource(Email, "/email/<int:email_id>")
api.add_resource(GetEmails, "/gmail-emails")
api.add_resource(GetEmailsByTime, "/gmail-emails-by-time")
api.add_resource(GetEmailsBySender, "/gmail-emails-by-sender")
api.add_resource(ClassifyEmail, "/classify-emails")

if __name__ == "__main__":
    app.run(debug=True)
