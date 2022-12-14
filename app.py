from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "SecretPhrase"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

user_responses = []  # will hold the clients answers
satisfaction_survey = surveys["satisfaction"]  # get satisfaction survey

# list of dicts consisting of questions and choices [list]
SATISFACTION_DICT_QUESTIONS_CHOICES = [{
    'question': satisfaction_question.question,
    'choices': satisfaction_question.choices
} for satisfaction_question in satisfaction_survey.questions]

LENGTH = len(SATISFACTION_DICT_QUESTIONS_CHOICES)

current_idx = 0  # what index are we currently in


# home route
@app.route('/')
def home():
    """ Returns a title and instructions to the user """
    if current_idx >= LENGTH:  # render completed page route when end of index hits
        return redirect('/thankyou')
    # user_responses.clear()  # clear out the list fresh start
    # current_idx = 0  # reset to 0

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('index.html',
                           title=title,
                           instructions=instructions)


@app.route('/questions/<int:idx>')
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
        answer = request.form.get('answer')
        user_responses.append(answer)

        return render_template('answer.html',
                               response=answer,
                               url=f'/questions/{current_idx}')

    if request.method == 'GET' and current_idx < LENGTH:
        flash("Please finish survey",
              'error')  # send error flash message to user
        return redirect(f'/questions/{current_idx + 1}')


@app.route('/thankyou')
def complete():
    print('finihsed route', current_idx, 'LENGTH', LENGTH)  # debugging
    if current_idx < LENGTH:  # did the user not finish question send back to question
        return redirect(f'/questions/{current_idx}')
    print('\n', user_responses, '\n')  # debugging
    flash("Finished!",
          'success')  # send a flash success message to user also for styles
    return render_template('finished.html')