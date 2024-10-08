import os
import json
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import base64  
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part, Tool
from vertexai.preview.generative_models import grounding
import time
from google.api_core.exceptions import ResourceExhausted
import os
from config import *


# Log in to Google Cloud
service_account_info = json.loads(google_credentials)
credentials = service_account.Credentials.from_service_account_info(service_account_info)

# Initialize Vertex AI
vertexai.init(project=vertex_project_id, location=server_location, credentials=credentials)
generation_config = {
    "max_output_tokens": max_output_tokens,
    "temperature": temperature,
    "top_p": top_p
}
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
    ),
]


# Define the model class

class google_vertex_chat:
    def __init__(self):
        self.model = GenerativeModel(
            vertex_model,
            system_instruction=[instructions]
        )
        self.chat = self.model.start_chat()
    def send_message(self, message, document=None):
        merged_msg = []
    
        if message:
            merged_msg.append(message)
        if document:
            if isinstance(document, list):
                merged_msg.extend(document)
            else:
                merged_msg.append(document) 
        return self.chat.send_message(
            merged_msg,
            generation_config=generation_config,
            safety_settings=safety_settings
        )