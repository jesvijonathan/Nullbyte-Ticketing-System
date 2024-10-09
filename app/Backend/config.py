import os
import secrets
from dotenv import load_dotenv

load_dotenv()

secret_key = ""

LDAP_SERVER = os.getenv("LDAP_SERVER", "ldap://DC01.nullbyte.exe") 
JWT_SECRET = os.getenv("JWT_SECRET") or secrets.token_urlsafe(32)

if not JWT_SECRET:
    raise ValueError("JWT_SECRET must be set in the environment variables")

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 36000

# Admin Creds
ADMIN_CRED = dict({
    'username': os.getenv('SVC_ACC', 'admin'),
    'password': os.getenv('SVC_ACC_PASS', 'admin')
})
ADMIN_CRED_2 = dict({
    'username': os.getenv('SVC_ACC', 'nig'),
    'password': os.getenv('SVC_ACC_PASS', 'nig')
})

# dict data | should convert/store to db 
users = {} # token, userid, 
users_token = {}
sockets = {} # connection_status, chat_object
socket_connection = {}

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
instructions_chat="""You are an IT application/expert engineer who has to sort and work on incoming tickets from merchant or clients for worldline\'s products in the payment/fintech industry. start with a greeting and understand the issue, ask specific questions only if required and try to auto fill or get all the details with minimal queries. Have a conversation and when the conversation ends (once the users sends a \'create\' text), provide the json as the last parameter, Do Not provide the json before the conversation ends & keep the conversation natural in a flow. Also give them an option to mention \"create\" to continue creating a ticket (only if the text/description is retrieved from user). Give brief replies. Do not nudge. Upon \"create\" command, just give the json & upon command \"status\", explain what you have understood till now. If any attachment is provided, go through it and analyse it, dont ask the user to explain the logs, understand and retrieve it yourself.
{
\\\"subject\\\" : \\\"\\\", // Generate the title for provided text, string
\\\"summary\\\": \\\"\\\", // Generate a summary of the text, with all description, string
\\\"attachments\\\": [ {\\\"attachment_name\\\" : \\\"The attachement name \\\", \\\"attachment details\\\" :  \\\" analysis, file information about the attachent and issue\\\" } ], // Mention the attachment name and details from it, if it is an image get the error/details or the situation, if it is a log file try to get the error or cause or description from the logs. Do the analysis & try fetching whatever went wrong is is the cause. and give an explanation.
\\\"product_type\\\": \\\"\\\", // retrieve the product type from the text & attachments, string: [ webgui, wlpfo, pass, wlsi, ]
\\\"issue_type\\\": \\\"\\\", // retrieve the issue type from the text & attachments, string: [\'bug\', \'error\', \'issue\', \'story\', \'others\', \'feature\', \'enhancement\', \'support\']
\\\"priority\\\": \\\"\\\", // Analyse the priority from the text & attachments, string: [\'crtical\', \'high\', \'medium\', \'low\']\\
\\\"story_points\\\": \\\"\\\", // Analyse the story points from the text & attachments, linked with the priority & ticket type, int: 'n'
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
instructions_enhance="""receive an text string and enhance the message with better words and better explanation & considering all parameters. In the end, return one single plain enhanced string""" 
instructions_autofill="""You are an ai/machine learning system, who has to enhance incoming tickets from merchant/clients or ticketing system for worldline\'s products in the payment/fintech industry. Auto fill or get all the details from provided resources. provide the json as the last parameter, explain properly and naturally.
Strictly just give a json, starting with `{` & ending with `}`

json format:
{
"chat_id": "", // do not modify, use the incoming values
"ticket_id": "", // do not modify, use the incoming values
"user": "", // do not modify, use the incoming values
"medium": "", // do not modify, use the incoming values
"connection: "", // do not modify, use the incoming values
"text": "", // do not modify, use the incoming values
"subject" : "", // Generate the title for provided text, string
"summary": "", // Generate a summary of the text, with all description, string
"attachments": [] // do not modify, use the incoming values
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
google_credentials="""
{
  "type": "service_account",
  "project_id": "silken-fortress-437417-p4",
  "private_key_id": "c6e7e43d39563d928ddc6bfd02eb17820109ecf5",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDpLFXAdX8S6bHO\\nETRexiJi/6jhuIzAR6cR9SLrZw6AC9s/dBk63jPoIRas4gcaQM1dUEBLcbs7oCwD\\nxZIO9tcfz79L7LARSOgososnMsReZ99cH7+oIn5wjJQbTguMlrudxhL1eqteV6z+\\nda7fUYrqLVj9ixtmxZ76KqVwOeLV/Caz3J/kPAr+W7memEdWSPFkgR41/jbYwiEh\\n0r+6PPMcBTb5qDknuX4RZZojW2AXbJnsMu8oglUXtvITyJcpk+9wNBGqz4OILLZe\\nii4AmpuzQn98YDEju53XKi2oIgqqn2Aovj5z3FC4XrdVP8MGnnWZ+J3lsQUPHTwy\\n1H22BEElAgMBAAECggEAAzPQGAT/wjP89JT7veXP5kGszAV+Q2FzNosswq8R6H7L\\n26bTIOHuibyImfEUbWR18uyNptZF9ByaoND3alFdZNW0LXgE9rEkZR4HTLoaWdHo\\njqnt9oJwxPLH/EmvCBba4UttimW3/E33ytqKv2JDO5JKCQNpKdkYJPHt1JPVnSA4\\ndUZxB6DoPPQpqpFB8wBmCqeI9/XnApKFVe2pN7zrxnCbPnLqApvUnfLKluc+LIWq\\nE+IjdjFyf18RcpJOejSna1PF6AS3EBMz/bv0ic958EJUI+G+ZVZVOX9auPWPAsK+\\n1qS+clAr7ezvrXfQ+INb15X6+tG7Zmpcxst2NkZaoQKBgQD+59nYlD9sD3+ipK2f\\nVFLmWlFnfVCKQQTCZzAKwI8Qxvv+Xx8/rd9BVG8Sfqt/RHmIKaDg4uezLKeLFRmk\\niB5ePJ0w3o1StYgX20Xk6Jg5ft7UcptcWDwaKCsLPAQcmakyZW2FRrIXdCa3l7zz\\nOt43/axzpxDZpoC7bJmaWAfFxQKBgQDqLJlu9P2tjIzkf2bGvvPr4YQ42Axq4Cmq\\nKWTH3tVX6FPB6hp9Xk8p6TFAXWq4DZv8P8uTc34KqMu3BNIngVqPMTZAcgQd9/36\\nkEU6KEm/yEgn1nz12/P3TOW2Fp3hFPEUFBEPJjXjD2cQhkO2RT73ZhJQjkwb6c4C\\nHb1Eqmej4QKBgQCs3lWJoHgmc5hOl7m7bPdPiv7b3Utqh0+P+2TEVfRwH1I0HxRV\\nHjhi2Lz+4PKzO5/j7L9S4+7YPzdchjG+uCVIKXk89CEJb1zdOPJ8nBToIRdDInok\\nNR6FaqpOUyRCtR7es5SDpv8OEtJS/c/BcDHV7O4v/KPbxyRUdwDwgDS9NQKBgA8K\\nGDyRDW3E9hOCvyYKg33luOkxrvJ6PRLJn8haXldL+30bvOHKWck2Scx5c24oqZj0\\nu+1XYIPsvVCexaR14UwK/BH9gJgwIiaid1+50Kq5gTDVzKa5npyGWsZsA22+O5Fv\\njHztlk5j4dmk1dpx7g5Tht+Xk/nC9VEbedlcHFXhAoGAE/yj1NNPzgiWf5A4TVEX\\nMj1XviGEwi0Oy5Bd1Y/GIzwY+VaR8bSB7xe9TJVkC0A7+Y+tAPl3gQjF6R60XYus\\n5w+fupegXSBgqgHXoFMDkWHtdQrAtvI5X61lCGQnzGEJnZZq/itz2c2TatkDTQY1\\nP3oMvIniJKsO+VhZRniiCWk=\\n-----END PRIVATE KEY-----\\n",
  "client_email": "nulllbyte@silken-fortress-437417-p4.iam.gserviceaccount.com",
  "client_id": "101967681156577996906",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/nulllbyte%40silken-fortress-437417-p4.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""
chatbot_fallback=2 # 0 - only wl_vertex, 1 - only wl_llama, 2 - wl_vertex priority & fallback to wl_llama, 3 - wl_llama priority & fallback to wl_vertex  
OLLAMA_MODEL = "jesvi"
chat_json= {
    "chat_id": "", # 1234567890
    "ticket_id": "", # SVC-123456
    "user": "", # username
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