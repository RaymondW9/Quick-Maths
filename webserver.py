from flask import Flask, render_template, request, session, url_for
import datetime
from random import randint

app = Flask(__name__)
app.secret_key = "a, b, c where a^n + b^n = c^n for n > 2"

@app.route('/', methods=['GET', 'POST'])
def start():
    session['points'] = 0
    session['num1'] = randint(0, 100)
    session['num2'] = randint(0, 100)
    session['started'] = 0
    session['time'] = 60
    if request.method == 'POST':
        try:
            session['time'] = int(request.form['time'])
            if session['time'] < 10 or session['time'] > 300:
                session['time'] = 60
        except:
            pass
    return render_template('start.html', url=url_for('quiz'), time=session['time'])

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
            if ans == session['num1'] + session['num2']:
                session['points'] = session['points'] + 1
        except:
            pass
    session['num1'] = randint(0, 100)
    session['num2'] = randint(0, 100)
    return render_template('quiz.html', num1=session['num1'], num2=session['num2'], points=session['points'])

app.run(host='0.0.0.0', port=5000, debug=True)