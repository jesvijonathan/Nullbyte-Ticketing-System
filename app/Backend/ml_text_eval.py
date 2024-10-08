from flask import Blueprint, request, jsonify, render_template
from flask_socketio import emit
from modules.auth.auth import jwt_required  
from config import *

# Initialize the Blueprint
text = Blueprint('text', __name__)

@text.route('/', methods=['GET', 'POST'])
@jwt_required
def text_test():
    return render_template('text.html')

# AI enhance api

# autofill api

# analyse log file