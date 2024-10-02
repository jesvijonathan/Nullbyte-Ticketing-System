from flask import Blueprint


text=Blueprint('text',__name__)

@text.post('/')
def text_test():
    pass