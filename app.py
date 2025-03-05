# from flask import flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return '<h3>My first flask app</h3>'

from flask import Flask
    
app = Flask(__name__)

@app.route('/')
def home():
    return 'Authors API project setup'

if __name__ == '__main__':
    app.run(Debug=True)

