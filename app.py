from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "SecretPhrase"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

satisfaction_survey = surveys["satisfaction"]  # get satisfaction survey

# list of dicts consisting of questions and choices [list]
SATISFACTION_DICT_QUESTIONS_CHOICES = [{
    'question': satisfaction_question.question,
    'choices': satisfaction_question.choices
} for satisfaction_question in satisfaction_survey.questions]

LENGTH = len(SATISFACTION_DICT_QUESTIONS_CHOICES)

current_idx = 0  # what index are we currently in


@app.before_request
def print_cookies():
    print('****************')
    print('COOKIES', session.get('user_resp_cookie'))
    print('****************')


# home route
@app.route('/', methods=['GET', 'POST'])
def home():
    """ Returns a title and instructions to the user """
    if request.method == 'POST':  # set cookies and reset user responses
        session.clear()
        session['user_resp_cookie'] = []
        return redirect('/questions/0')

    if current_idx >= LENGTH:  # render completed page route when end of index hits
        return redirect('/thankyou')
    # current_idx = 0  # reset to 0

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('index.html',
                           title=title,
                           instructions=instructions)


@app.route('/questions/<int:idx>', methods=['GET', 'POST'])
def questions(idx):
    """ Returns questions """
    global current_idx  # used to modify global variable

    if idx != current_idx:  # check if user is trying to skip a question
        flash("Cant't access invalid question", 'error')  # send error to user

    idx = current_idx
    if idx >= LENGTH:  # render completed page route when end of index hits
        return redirect('/thankyou')

    next_idx = current_idx + 1  # send over the next index

    return render_template('questionaire.html',
                           data=SATISFACTION_DICT_QUESTIONS_CHOICES[idx],
                           curr_page=next_idx,
                           out_of=LENGTH)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    """ Render the users answer """
    global current_idx  # used to modify global variable

    if current_idx >= LENGTH:  # did the user finish all questions
        return redirect('/thankyou')

    if request.method == 'POST':  # user successfully answered question
        current_idx += 1  # increase index and send next question to user
        answer = request.form.get('answer', 'none')

        # extract users answers from browser cookie
        response_from_user = session.get('user_resp_cookie', [])
        # append to extracted browser cookie list
        response_from_user.append(answer)
        # rebind browser cookie
        session['user_resp_cookie'] = response_from_user

        return render_template('answer.html',
                               response=answer,
                               url=f'/questions/{current_idx}')

    if request.method == 'GET' and current_idx < LENGTH:
        flash("Please finish survey",
              'error')  # send error flash message to user
        return redirect(f'/questions/{current_idx + 1}')


@app.route('/thankyou')
def complete():
    if current_idx < LENGTH:  # did the user not finish question send back to question
        return redirect(f'/questions/{current_idx}')
    # send a flash success message to user and use success as a class for styling
    flash("Finished!", 'success')
    return render_template('finished.html')