from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "SecretPhrase"
debug = DebugToolbarExtension(app)


@app.route('/')
def home():
    return render_template('base.html')