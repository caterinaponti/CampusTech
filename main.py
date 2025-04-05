from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

import secrets


app = Flask(__name__)
app.secret_key = '0ad399ba1c7e106f462428c079682c9c'

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
    balance = None
    building = None
    error = None

    if request.method == 'POST':
        student_id = request.form['student_id']
        action = request.form['action']

    # Read the balances.txt file and find the matching student ID
        try:
            with open('balances.txt', 'r') as file:
                for line in file:
                    parts = line.strip().split(' ')
                    if parts[0] == student_id:
                        balance = parts[1]
                        building = parts[2]
                        break
                else:
                    error = "Student ID not found."
        except FileNotFoundError:
            error = "balances.txt file not found."

        if error:
            return render_template('student_action.html', username=username, error=error)

        # Redirect to corresponding page, passing the necessary data
        if action == 'donate':
            return redirect(url_for('donate', username=username, student_id=student_id, balance=balance, building=building))
        elif action == 'request':
            return redirect(url_for('request_page', username=username, student_id=student_id, balance=balance, building=building))

    return render_template('student_action.html', username=username)

@app.route('/donation-success')
def donation_success():
    total_donation = request.arts.get('total_donation', 0, type=int)
    meal_count = request.arts.get('meal_count', 0, type=int)
    snack_count = request.arts.get('snack_count', 0, type=int)
    return render_template('donation_success.html', donation_amount=donation_amount)

@app.route('/donate/<username>/<student_id>/<balance>/<building>', methods=['GET', 'POST'])
<<<<<<< Updated upstream
<<<<<<< Updated upstream

@app.route('/donate/<username>/<student_id>/<balance>/<building>')

def donate(username, student_id, balance, building):
    '''
    studentBal = random number
    ## need student balance as a variable
    ## need the student balance - amount they're donating as a variable
    ## need the amount donating as a variable 
    # maybe make $10 and $25 final variables snack and meal 
    
    '''
    
=======
def donate(username, student_id, balance, building):
>>>>>>> Stashed changes
=======
def donate(username, student_id, balance, building):
>>>>>>> Stashed changes
    if 'donation_total' not in session:
        session['donation_total'] = 0
    # might need snack and meal counts but idk
    if 'meal_count' not in session:
        session['meal_count'] = 0
    if 'snack_count' not in session:
        session['snack_count'] = 0
    donation_amount = 0
    if request.method == 'POST':
        if 'meal' in request.form:
            session['meal_count'] += 1
            if donation_amount + 25 <= 50:
                session['donation_total'] += 25
            else:
                error = "Donation limit reached. You cannot donate more than $50."  
            
        elif 'snack' in request.form:
            session['snack_count'] += 1
            if donation_amount + 10 <= 50:
                session['donation_total'] += 10
            else:
                error = "Donation limit reached. You cannot donate more than $50."  
        elif 'reset' in request.form:
            session['donation_total'] = 0

        elif 'finish' in request.form:
            if session['donation_total'] + donation_amount >= 50:
                error = "Donation limit reached. You cannot donate more than $50."     
                return render_template('donate.html', username=username, student_id=student_id, balance=balance,building=building,error=error)
            else:
                session['donation_total'] += donation_amount

             #update the new balance

                new_balance = float(balance) -  session['donation_total']
                return redirect(url_for('donation_success', donation_amount=donation_amount))
    

<<<<<<< Updated upstream
<<<<<<< Updated upstream
    session['donation_total'] += donation_amount

    #update the new balance

    new_balance = float(balance) -  session['donation_total']
    return redirect(url_for('donation_success', donation_amount=donation_amount))


    Toler_balance = 3010
    LME_balance = 2030

    # Toler_balance = 3010
    # LME_balance = 2030


    # Toler_balance_check = {
    #     "January": Toler_balance,
    #     "February": 2744,
    #     "March":2060,
    #     "April":1200,
    #     "May":521,
    #     "June":0,
    #     "July":0,
    #     "August":Toler_balance,
    #     "September":2744,
    #     "October": 2060,
    #     "Novemeber":1200,
    #     "December":521
    # }

    # LME_balance_check = {
    #     "January": LME_balance,
    #     "February": 1776,
    #     "March":1269,
    #     "April":762,
    #     "May":250,
    #     "June":0,
    #     "July":0,
    #     "August":LME_balance,
    #     "September":1776,
    #     "October": 1269,
    #     "Novemeber":762,
    #     "December":250
    # }
    return render_template('donate.html', username=username, student_id=student_id, balance=balanace,building=building)
=======
    return render_template('donate.html', username=username, student_id=student_id, balance=balance,building=building)
>>>>>>> Stashed changes
=======
    return render_template('donate.html', username=username, student_id=student_id, balance=balance,building=building)
>>>>>>> Stashed changes
 

@app.route('/request/<username>/<student_id>/<balance>/<building>', methods=['GET', 'POST'])
def request_page(username, student_id, balance, building):
    Toler_balance = 3010
    LME_balance = 2030

    Toler_balance_check = {
        "January": Toler_balance, "February": 2744, "March": 2060,
        "April": 1200, "May": 521, "June": 0, "July": 0,
        "August": Toler_balance, "September": 2744, "October": 2060,
        "Novemeber": 1200, "December": 521
    }

    LME_balance_check = {
        "January": LME_balance, "February": 1776, "March": 1269,
        "April": 762, "May": 250, "June": 0, "July": 0,
        "August": LME_balance, "September": 1776, "October": 1269,
        "Novemeber": 762, "December": 250
    }

    current_month = datetime.now().strftime("%B")
    try:
        current_balance = float(balance)
    except ValueError:
        return f"Invalid balance format for student {student_id}."

    if building == "Toler":
        threshold = Toler_balance_check.get(current_month, 0)
    elif building == "LME":
        threshold = LME_balance_check.get(current_month, 0)
    else:
        return f"Unknown building: {building}"

    needs_flexi = current_balance < threshold
    queue_file = 'queue.txt'
    success_message = None
    error = None

    if request.method == 'POST' and needs_flexi:
        request_type = None
        amount = 0

        if 'meal' in request.form:
            request_type = 'meal'
            amount = 25
        elif 'snack' in request.form:
            request_type = 'snack'
            amount = 10
        else:
            error = "Please select an item to request."
            return render_template(
                'request.html',
                username=username,
                student_id=student_id,
                building=building,
                balance=current_balance,
                month=current_month,
                threshold=threshold,
                eligible=needs_flexi,
                error=error
            )

        with open(queue_file, 'a') as f:
            f.write(f"{username},{request_type},{amount},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        success_message = f"✅ {username}, your request for a ${amount} {request_type} was received and you're added to the queue."

    return render_template(
        'request.html',
        username=username,
        student_id=student_id,
        building=building,
        balance=current_balance,
        month=current_month,
        threshold=threshold,
        eligible=needs_flexi,
        success_message=success_message,
        error=error
    )

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)

def send_email(username, subject, message_body):
    sender_email = "cponti@dons.usfca.edu"
    sender_password = "your_app_password"  # Use app password, not your real password
    recipient_email = f"{username}@dons.usfca.edu"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message_body, 'plain'))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully to", recipient_email)
        return True
    except Exception as e:
        print("Failed to send email:", e)
        return False

if __name__ == '__main__':
    app.run(debug=True)


