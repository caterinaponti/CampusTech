from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

# Fake login credentials
USERNAME = "admin"
PASSWORD = "password123"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == USERNAME and pw == PASSWORD:
            return redirect(url_for('welcome', username=user))
        else:
            error = 'Invalid credentials. Please try again.'
    return render_template('login.html', error=error)


@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)

