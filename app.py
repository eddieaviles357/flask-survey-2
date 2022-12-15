from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretPhrase'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

satisfaction_survey = surveys["satisfaction"]  # get satisfaction survey

# list of dicts consisting of questions and choices [list]
SATISFACTION_DICT_QUESTIONS_CHOICES = [{
    'question': satisfaction_question.question,
    'choices': satisfaction_question.choices
} for satisfaction_question in satisfaction_survey.questions]

LENGTH = len(SATISFACTION_DICT_QUESTIONS_CHOICES)

# @app.before_request
# def print_cookies():
#     print('****************')
#     print('COOKIES', session.get('user_resp_cookie'))
#     print('****************')


# home route
@app.route('/', methods=['GET', 'POST'])
def home():
    """ Returns a title and instructions to the user """
    user_resp_length = len(session.get('user_resp_cookie', []))

    if request.method == 'POST':  # set cookies and reset user responses
        session.clear()
        session['user_resp_cookie'] = []
        return redirect('/questions/0')

    return render_template('index.html',
                           title=satisfaction_survey.title,
                           instructions=satisfaction_survey.instructions)


@app.route('/questions/<int:idx>', methods=['GET', 'POST'])
def questions(idx):
    """ Returns questions """
    user_resp_length = len(session.get('user_resp_cookie', []))

    if user_resp_length >= LENGTH:  # render completed page route when end of index hits
        flash('Finished!', 'success')
        return redirect('/thankyou')

    if idx != user_resp_length:  # check if user is trying to skip a question
        flash("Cant't access invalid question", 'error')  # send error to user

    return render_template(
        'questionaire.html',
        data=SATISFACTION_DICT_QUESTIONS_CHOICES[user_resp_length],
        curr_page=user_resp_length + 1,
        out_of=LENGTH)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    """ Render the users answer """
    user_resp_length = len(session.get('user_resp_cookie', []))

    if user_resp_length >= LENGTH:  # did the user finish all questions
        flash('Finished!', 'success')
        return redirect('/thankyou')

    if request.method == 'POST':  # user successfully answered question
        answer = request.form.get('answer', 'none')

        # extract users answers from browser cookie
        response_from_user = session.get('user_resp_cookie')
        # append to extracted browser cookie list
        response_from_user.append(answer)
        # rebind browser cookie
        session['user_resp_cookie'] = response_from_user
        user_resp_length += 1  # cookie list has increased by one

        return render_template('answer.html',
                               response=answer,
                               url=f'/questions/{user_resp_length}')

    # redirect to quesitons if user is trying to enter invalid url
    if request.method == 'GET':
        flash('Please finish survey',
              'error')  # send error flash message to user
        return redirect(f'/questions/{user_resp_length}')


@app.route('/thankyou')
def complete():
    user_resp_length = len(session.get('user_resp_cookie', []))
    if user_resp_length < LENGTH:  # did the user not finish question send back to question
        flash('Please finish survey',
              'error')  # send error flash message to user
        return redirect(f'/questions/{user_resp_length}')
    return render_template('finished.html')