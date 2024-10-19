import os
import secrets
from dotenv import load_dotenv
import json

load_dotenv()

secret_key = ""
CLOUD_SQL_CONNECTION_NAME = os.getenv("CLOUD_SQL_CONNECTION_NAME", "")
useCloudSql = False
LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://dc01.nullbyte.exe") 
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)
noSql =True
if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in the environment variables")

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000

# Admin Creds
ADMIN_CRED = dict({
    'username': os.getenv('ADMIN_ACC', 'admin'),
    'password': os.getenv('ADMIN_ACC_PASS', 'admin')
})
ADMIN_CRED_2 = dict({
    'username': os.getenv('SVC_ACC', 'nig'),
    'password': os.getenv('SVC_ACC_PASS', 'nig')
})

MAIL_CRED = dict({
    'username': os.getenv('MAIL_ACC', 'nig'),
    'password': os.getenv('MAIL_ACC_PASS', 'nig')
})

# dict data | should convert/store to db 
users = {} # token, userid, 
users_token = {}
sockets = {} # connection_status, chat_object
socket_connection = {}
mailchains={}

# Database configuration
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "3306")
DATABASE_USER = os.getenv("DATABASE_USER", "nullbyteadmin")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "rootpassword")
DATABASE_NAME = os.getenv("DATABASE_NAME", "nullbyte")
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


# Gen AI/ML Config
vertex_project_id = "silken-fortress-437417-p4"
vertex_model="gemini-1.5-pro-002" # gemini-1.5-flash-002 #gemini-1.5-pro-002 #codechat-bison-32k@002
server_location = "asia-southeast1"
max_output_tokens = 1024
temperature=0.2
top_p = 0.8
default_greet_msg="Hello! How can I help you today?"
default_reply_msg="Thank you for providing the details. I have created a ticket to investigate the issue."
instructions_chat="""You are an IT application/expert engineer who has to sort and work on incoming tickets from merchant or clients for worldline\'s products in the payment/fintech industry. start with a greeting and understand the issue, ask specific questions only if required and try to auto fill or get all the details with minimal queries. Have a conversation and when the conversation ends (once the users sends a \'create\' or /create command/text ), provide the json as the last parameter, Do Not provide the json before the conversation ends & keep the conversation natural in a flow. Also give them an option to mention \"create\" to continue creating a ticket (only if the text/description is retrieved from user). Give brief replies. Do not nudge. Upon \"create\" command, STRICTLY give just the json & upon command \"status\", explain what you have understood till now. If any attachment is provided, go through it and analyse it, dont ask the user to explain the logs, understand and retrieve it yourself.
{
\\\"subject\\\" : \\\"\\\", // Generate the title for provided text, string
\\\"description\\\" : \\\"\\\", // Generate the description for provided text, string
\\\"summary\\\": \\\"\\\", // Generate a summary of the text, with all description, string
\\\"attachments\\\": [ {\\\"attachment_name\\\" : \\\"The attachement name \\\", \\\"attachment details\\\" :  \\\" analysis, file information about the attachent and issue\\\" } ], // Mention the attachment name and details from it, if it is an image get the error/details or the situation, if it is a log file try to get the error or cause or description from the logs. Do the analysis & try fetching whatever went wrong is is the cause. and give an explanation.
\\\"product_type\\\": \\\"\\\", // retrieve the product type from the text & attachments, string: [ webgui, wlpfo, pass, wlsi, ]
\\\"issue_type\\\": \\\"\\\", // retrieve the issue type from the text & attachments, string: [\'bug\', \'error\', \'issue\', \'story\', \'others\', \'feature\', \'enhancement\', \'support\']
\\\"priority\\\": \\\"\\\", // Analyse the priority from the text & attachments, string: [\'crtical\', \'high\', \'medium\', \'low\']\\
\\\"status\\\": \\\"\\\", // always string: 'open'
\\\"story_points\\\": \\\"\\\", // Analyse the story points from the text, description & attachments, linked with the priority & ticket type, int: 'n'
\\\"estimation\\\": \\\"\\\", // Analyse the estimation from the text & attachments, linked with the story points & priority, n hours in int: 'n'
\\\"analysis\\\": \\\"\\\", // Analysis of the issue, what could be the possible cause of the issue, and how can it be resolved from an support or engineer\'s point of view. If an legit error/bug, give solution on worldline\'s product. string
\\\"reply\\\": \\\"\\\" // Possible reply to the support text. string
}

/status: <none>, 
return a <string: give the current status, analysis and a proper description of the problem>

/enhance_text: <string: a text description about a ticket or problem>
return a <string: give the enhacened description with proper formating and added information that suites better for the ticket descritpion?

/fill_ticket <json: ticket details>
return a <json: enahance and autofill empty variables with the description/text provided>
"""
instruction_analyse_attachments="""receive an attachment and analyse it, describe it, get the error or cause or description from the logs. Do the analysis & try fetching whatever went wrong is is the cause. and give an short explanation.return the json with the analysis and description of the attachment

input : string and attachment
return result json format:
{
"attachment": "", // derived attachement name
"format": "", // The format of the attachment, string: [\'image\', \'log\', \'text\', \'pdf\', \'doc\', \'others\']
"details": "" // Do full analysis, file information about the attachent and explain the attachment and give a description about the input file/attachment
"analysis": "" // Analysis of the issue, what could be the possible cause of the issue, and how can it be resolved from an support or engineer\'s point of view. If an legit error/bug, give solution on worldline\'s product. string
"reply": "" // Possible reply to the support text. string
}
"""
instructions_enhance="""receive an text string and enhance the message with better words and better explanation & considering all parameters. In the end, return one single plain enhanced string""" 
instructions_autofill="""You are an ai/machine learning system, who has to enhance incoming tickets from merchant/clients or ticketing system for worldline\'s products in the payment/fintech industry. Auto fill or get all the details from provided resources. provide the json as the last parameter, explain properly and naturally.
Strictly just give a json, starting with `{` & ending with `}`

json format:
{
"chat_id": "", // do not modify, use the incoming values
"ticket_id": "", // do not modify, use the incoming values
"user": "", // do not modify, use the incoming values
"medium": "", // do not modify, use the incoming values
"description":"",do not modify, use the incoming values
"connection: "", // do not modify, use the incoming values
"text": "", // do not modify, use the incoming values
"subject" : "", // Generate the title for provided text, string
"summary": "", // Generate a summary of the text, with all description, string
"attachments": [] // do not modify, use the incoming values
"status":,"open" // always string: 'open'
"product_type": "", // retrieve the product type from the text & attachments, string: [ webgui, wlpfo, pass, wlsi, ]
"issue_type": "", // retrieve the issue type from the text & attachments, string: [\'bug\', \'error\', \'issue\', \'story\', \'others\', \'feature\', \'enhancement\', \'support\']
"priority": "", // Analyse the priority from the text & attachments, string: [\'crtical\', \'high\', \'medium\', \'low\']\\
"story_points": "", // Analyse the story points from the text & attachments, linked with the priority & ticket type, int: 'n'
"estimation": "", // Analyse the estimation from the text & attachments, linked with the story points & priority, n hours in int: 'n'
"analysis": "", // Analysis of the issue, what could be the possible cause of the issue, and how can it be resolved from an support or engineer\'s point of view. If an legit error/bug, give solution on worldline\'s product. string
"reply": "" // Possible reply to the support text. string
"enhance": "", receive the text/summary/analysis and enhance the message with better words and better explanation & considering all parameters. 
}
"""


google_credentials = os.getenv("GOOGLE_CREDENTIALS", "").strip()

# Check if credentials are not provided or set to "null"
if not google_credentials or google_credentials == "null":
    try:
        with open('./google_credentials.json', 'r') as file:
            google_credentials = file.read()
            google_credentials = str(google_credentials)
    except FileNotFoundError:
        google_credentials = None

if not google_credentials:
    raise ValueError("GOOGLE_CREDENTIALS must be set in the environment variables or in ./google_credentials.json")


# At this point, google_credentials is guaranteed to be a dictionary
service_account_info = google_credentials  # Use it directly as it should be a dict now

chatbot_fallback=2 # 0 - only wl_vertex, 1 - only wl_llama, 2 - wl_vertex priority & fallback to wl_llama, 3 - wl_llama priority & fallback to wl_vertex  
OLLAMA_MODEL = "nullbyte"
ollama_amnesia = 0 # 0 - no amnesia, 1 - amnesia
chat_json= {
    "chat_id": "", # 1234567890
    "ticket_id": "", # SVC-123456
    "user": "", # username
    "description":"",#description
    "medium": "", # [ "chat (vertex/ollama)", "email", "form" ]
    "connection": "live", # [ "live", "offline", "closed" ]
    "text": "", # "I am experiencing timeouts with EFTPOS transactions."
    "subject": "", # WLPFO EFTPOS Transaction Timeouts for Overseas Purchases during High TPS
    "summary": None, # WLPFO is experiencing timeouts for EFTPOS transactions, specifically for overseas purchases and during periods of high throughput (200+ TPS). This issue requires batch processing as a workaround. The timeouts seem to occur regardless of card type or amount but are specific to transactions made with overseas acquirers or gateways.
    "attachments": [], # [ { "type": "image", "file_name": "screenshot_1", "details": "The error message displayed is 'Transaction Timeout'." } ]
    "product_type": None, # [ "webgui", "wlpfo", "pass", "wlsi" ]
    "issue_type": None, # [ "bug", "error", "issue", "story", "others", "feature", "enhancement", "support" ]
    "priority": None, # [ "critical", "high", "medium", "low" ]
    "story_points": None, # 5
    "estimation": None, # 3
    "analysis": None, # The issue seems to be related to high-volume EFTPOS transactions routed to overseas acquirers or gateways. This could indicate a bottleneck in communication or processing on either Worldline's end or the acquiring bank's side. Further investigation is needed to pinpoint the exact cause, including reviewing network latency, transaction logs, and potential rate limiting by acquirers.
    "reply": default_reply_msg, # Thank you for providing the details. I have created a ticket to investigate the EFTPOS transaction timeouts you are experiencing with WLPFO for overseas purchases during high TPS. Our team will analyze the issue and provide updates as they become available.
}

# bucket paths 
tmp_folders_cleanup=False
attachment_upload_folder='./bucket/attachments/'
chats_folder='./bucket/chats/'
ticket_folder = "./bucket/tickets"

bucket_name="nullbyte"
bucket_mode=True

baseMyURL = "http://localhost:5000"


if os.name == 'nt':
    ticket_folder = ticket_folder.replace("/", "\\")
    attachment_upload_folder = attachment_upload_folder.replace("/", "\\")
    chats_folder = chats_folder.replace("/", "\\")


# Jira Configs

JIRA_CRED = dict({
    'username': os.getenv("JIRA_ADMIN",'jiraadmin'),
    'password': os.getenv("JIRA_PASS", 'Skibbidi@42069'),
    'server': os.getenv("JIRA_SERVER", 'http://localhost:8080')
})

db_add_closed_chat = False


# tmp DB 
ticket_db={}
old_chat = {}