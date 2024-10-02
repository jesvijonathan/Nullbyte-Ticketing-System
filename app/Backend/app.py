from flask import Flask, request
from flask_cors import CORS
from auth import auth_ldap
from ml_image_eval import vision
from ml_text_eval import text
from modules.ticket import ticket
from config import *

#flask configurations
app = Flask(__name__)
app.config.from_prefixed_env()
CORS(app, resources={r"/*": {"origins": "*"}})

# app configurations
app.register_blueprint(auth_ldap,url_prefix='/sso')
app.register_blueprint(ticket,url_prefix='/v1/ticket')

# a demo page to pass screenshots 
# # and on submit evaluate the screen shot and find the product/division
app.register_blueprint(vision,url_prefix='/v1/vision')


# get text and other details
# get product, division, team, issue, summary, issue-level, 
app.register_blueprint(text,url_prefix='/v1/text')

if __name__ == '__main__':
    app.run(debug=True) 
