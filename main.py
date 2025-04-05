from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']

        # Read stored credentials
        try:
            with open('users.txt', 'r') as file:
                users = [line.strip().split(',') for line in file]
        except FileNotFoundError:
            users = []

        # Check if user exists
        if [user, pw] in users:
            return redirect(url_for('student_action', username=user))
        else:
            # Register new user
            with open('users.txt', 'a') as file:
                file.write(f'{user},{pw}\n')
            return redirect(url_for('student_action', username=user))

    return render_template('login.html', error=error)

@app.route('/student-action/<username>', methods=['GET', 'POST'])
def student_action(username):
    if request.method == 'POST':
        student_id = request.form['student_id']
        action = request.form['action']
        
        if action == 'donate':
            return redirect(url_for('donate', username=username, student_id=student_id))
        elif action == 'request':
            return redirect(url_for('request_page', username=username, student_id=student_id))

    return render_template('student_action.html', username=username)

@app.route('/donate/<username>/<student_id>')
def donate(username, student_id):
    return render_template('donate.html', username=username, student_id=student_id)

@app.route('/request/<username>/<student_id>')
def request_page(username, student_id):
    return render_template('request.html', username=username, student_id=student_id)

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
