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
    sur_lst = [surv for surv in surveys.values()]
    return render_template('index.html', survey=sur_lst[0])
