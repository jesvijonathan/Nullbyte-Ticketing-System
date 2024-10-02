from flask import Blueprint


vision=Blueprint('vision',__name__)

@vision.post('/')
def vision_test():
    pass