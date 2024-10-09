from flask import Blueprint, request, jsonify, render_template, session, make_response
from flask_socketio import emit
from modules.auth.auth import jwt_required  
from config import *
import modules.ml.wl_vertex as wl_vertex
from modules.log import *
import json

# Initialize the Blueprint
text = Blueprint('text', __name__)

@text.route('/', methods=['GET', 'POST'])
@jwt_required
def text_test():
    return render_template('text.html')

# pass an description text, and get enhanced version of it 
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
            logger.error(f"An error occurred: {str(e)}")
            return make_response(jsonify({'error': 'Server error occurred'}), 500)
        
# pass an partially filled ticket json (summary/description) mandatory, and get is autofilled
@text.route('/fill_ticket', methods=['GET', 'POST'])
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
            return jsonify({'result': json_msg})

        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return make_response(jsonify({'error': str(e)}), 500)