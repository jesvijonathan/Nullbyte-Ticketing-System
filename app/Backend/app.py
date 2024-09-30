from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import datetime
import jwt
from ldap_wrapper import Lwrapper;
from config import *
app = Flask(__name__)
CORS(app)

@app.route("/sso/auth", methods=["POST"])
def authenticate():
    if not request.is_json:
        return make_response(jsonify({'error': 'Request must be JSON'}), 400)

    body = request.json
    username = body.get('email')
    password = body.get('password')

    if not username or not password:
        return make_response(jsonify({'error': 'email and password are required'}), 400)

    logger.info(f"Authenticating user: {username}")
    
    if Lwrapper().Authenticate(username,password):
        payload = {
        'sub': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    if token:
        return make_response(jsonify({'token': token}), 201)
    
# a demo page to pass screenshots
# and on submit evaluate the screen shot and find the product/division
@app.route("/vision")
def vision_test():
    pass

# get text and other details
# get product, division, team, issue, summary, issue-level, 
@app.route("/text")
def text_test():
    pass

if __name__ == '__main__':
    app.run(debug=True)
