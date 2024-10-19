from flask import Blueprint, request, jsonify, render_template, session, make_response
from flask_socketio import emit
from modules.auth.auth import jwt_required  
from config import *
from modules.bucket import *
import modules.ml.wl_vertex as wl_vertex
from modules.log import *
import json
import base64
import os

# Initialize the Blueprint
text = Blueprint('text', __name__)

@text.route('/', methods=['GET', 'POST'])
@jwt_required
def text_test():
    return render_template('text.html')

# pass an description text, and get enhanced version of it 
@jwt_required
@text.route('/enhance_text', methods=['GET', 'POST'])
def enhance():
    if request.method == 'GET':
        return render_template('enhance.html')

    elif request.method == 'POST':
        try:
            data = request.get_json()
            to_enhance_string = data.get("to_enhance_string", "")
            if not to_enhance_string:
                return make_response(jsonify({'error': 'Please pass a non-empty text/string'}), 400)

            enhance = wl_vertex.google_vertex_chat(instruction=instructions_enhance)
            response = enhance.send_message(message=to_enhance_string)

            if response is None or not hasattr(response, 'candidates') or not response.candidates:
                return make_response(jsonify({'error': 'Failed to enhance the message'}), 500)
            if len(response.candidates) == 0:
                return make_response(jsonify({'error': 'No candidates received in response'}), 500)

            text_response = response.candidates[0].content.parts[0].text
            return jsonify({'result': text_response})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return make_response(jsonify({'error': 'Server error occurred'}), 500)
        
# pass an partially filled ticket json (summary/description) mandatory, and get is autofilled
@text.route('/fill_ticket', methods=['GET', 'POST'])
# @jwt_required
def fill_ticket():
    if request.method == 'GET':
        return render_template('fill_ticket.html')

    if request.method == 'POST':
        try:
            data = request.data
            json_data = json.loads(data)

            fill = wl_vertex.google_vertex_chat(instruction=instructions_autofill)
            response = fill.send_message(message=json.dumps(json_data))
            
            filled_ticket=None
            if response and hasattr(response, 'candidates') and response.candidates:
                filled_ticket=response.candidates[0].content.parts[0].text
            json_msg = ""
            if "```json" in filled_ticket:
                start_index = filled_ticket.index("```json") + len("```json")
                end_index = filled_ticket.index("```", start_index)
                json_msg = filled_ticket[start_index:end_index].strip()  
            else:
                return make_response(jsonify({'error': 'Failed to fill the ticket'}), 500)
            
            print("Filled Ticket JSON:", json_msg)            
            return jsonify({'result': json.loads(json_msg)})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return make_response(jsonify({'error': str(e)}), 500)
        
# pass an text, document, logs, etc file to get the analysis of it
@text.route('/attachment', methods=['GET', 'POST'])
def attachment():
    try:
        if request.method == 'GET':
            return render_template('attachment.html')

        if request.method == 'POST':
            data = request.get_json()

            chat_id = data.get('chat_id', None)
            text = data.get('text', None)
            file_data = data.get('file', None)

            if not chat_id:
                return make_response(jsonify({'error': 'chat_id is required'}), 400)
            
            if not text and not file_data:
                return make_response(jsonify({'error': 'Please provide either text or an attachment'}), 400)

            chat_folder = os.path.join(attachment_upload_folder, str(chat_id))
            os.makedirs(chat_folder, exist_ok=True)

            attachment_data = None
            if file_data:
                filename = file_data.get('name', '')
                file_size = file_data.get('size', '')
                file_type = file_data.get('type', '')
                file_content = file_data.get('data', '')

                # Save file to server
                if filename and file_content:
                    file_path = os.path.join(chat_folder, filename)
                    with open(file_path, "wb") as f:
                        f.write(base64.b64decode(file_content))

                    attachment_data = {
                        "filename": filename,
                        "size": file_size,
                        "type": file_type,
                        "data": file_content
                    }
            print("Attachment Data:", attachment_data)
            # Send message to Vertex AI
            response = wl_vertex.google_vertex_chat(instruction=instruction_analyse_attachments).send_message(
                message=text,
                document=[attachment_data] if attachment_data else None
            )

            if response and hasattr(response, 'candidates') and response.candidates:
                result_message = response.candidates[0].content.parts[0].text
                json_msg = ""
                if "```json" in result_message:
                    start_index = result_message.index("```json") + len("```json")
                    end_index = result_message.index("```", start_index)
                    json_msg = result_message[start_index:end_index].strip() 
                return jsonify({'result': json.loads(json_msg)})
            else:
                return make_response(jsonify({'error': 'Failed to process the message'}), 500)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return make_response(jsonify({'error': 'Server error occurred'}), 500)