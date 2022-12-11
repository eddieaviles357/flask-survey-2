from flask import Flask, request, render_template
# from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "SecretPhrase"
# debug = DebugToolbarExtension(app)
# will hold the clients answers
responses = []


# home route
@app.route('/')
def home():
    """ Returns a questionaire to the user """
    return render_template('index.html', title=surveys["satisfaction"].title)