from flask import Blueprint
from flask import session

vision=Blueprint('vision',__name__)

@vision.post('/')
def vision_test():
    user = session.get('user')
    print("######################### : ", user)
    return "Vision test: {}".format(user)