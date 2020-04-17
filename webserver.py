from flask import Flask, render_template, request, session, url_for
import datetime
from random import randint

app = Flask(__name__)
app.secret_key = "a, b, c where a^n + b^n = c^n for n > 2"

@app.route('/', methods=['GET', 'POST'])
def start():
    session['points'] = 0
    session['started'] = 0
    session['time'] = 60
    session['mode'] = '+'
    session['min'] = 0
    session['max'] = 100
    if request.method == 'POST':
        #get the user-inputted duration
        try:
            session['time'] = int(request.form['time'])
            if session['time'] < 10 or session['time'] > 300:
                session['time'] = 60
        except:
            pass
        #get the user-inputted mode
        try:
            session['mode'] = request.form['mode']
        except:
            pass
        #get the user-inputted range
        try:
            session['min'] = int(request.form['min'])
            session['max'] = int(request.form['max'])
            if session['min'] < -100000 or session['max'] > 100000 or session['min'] > session['max']:
                session['min'] = 0
                session['max'] = 100
        except:
            pass
    if session['mode'] == '+':
        mode = 'addition'
    if session['mode'] == '-':
        mode = 'subtraction'
    if session['mode'] == '*':
        mode = 'multiplication'
    if session['mode'] == '/':
        mode = 'division'
    session['num1'] = randint(session['min'], session['max'])
    session['num2'] = randint(session['min'], session['max'])
    return render_template('start.html', url=url_for('quiz'), time=session['time'], mode=mode, minimum=session['min'], maximum=session['max'])

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    
    #if the challenge was started, record the end-time. Otherwise, prompt the user to return to the start page
    try:
        if session['started'] == 0:
            session['started'] = 1
            session['endtime'] = datetime.datetime.now() + datetime.timedelta(seconds=session['time'])
    except:
        return render_template('results.html', url=url_for('start'), score=-1)
    
    #after time's up, return the user's score
    if datetime.datetime.now() > session['endtime']:
        return render_template('results.html', url=url_for('start'), score=session['points'])
    
    #Check the user's answer
    if request.method == 'POST':
        try:
            ans = int(request.form['userAns'])
            if session['mode'] == '+':
                correctAns = session['num1'] + session['num2']
            if session['mode'] == '-':
                correctAns = session['num1'] - session['num2']
            if session['mode'] == '*':
                correctAns = session['num1'] * session['num2']
            if session['mode'] == '/':
                correctAns = session['num1'] / session['num2']
            if ans == correctAns:
                session['points'] = session['points'] + 1
        except:
            pass
    session['num1'] = randint(session['min'], session['max'])
    session['num2'] = randint(session['min'], session['max'])
    if session['mode'] == '/':
        #avoid dividing by 0
        if session['num2'] == 0:
            session['num2'] = 1
        #avoid decimal answers
        session['num1'] = randint(session['min'], session['max']) * session['num2']
    return render_template('quiz.html', num1=session['num1'], num2=session['num2'], points=session['points'], mode=session['mode'], url=url_for('start'))

app.run(host='0.0.0.0', port=5000, debug=True)
