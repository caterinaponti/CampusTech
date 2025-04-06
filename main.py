from flask import Flask, render_template, request, redirect, url_for, session
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
@app.route('/donation-failed')
def donation_failed():
    balance = request.args.get('balance',type=float)
    new_balance = float(balance) -  session['donation_total']
    donation_total = request.args.get('donation_total', 0, type=int)
    meal_count = request.args.get('meal_count', 0, type=int)
    snack_count = request.args.get('snack_count', 0, type=int)
    return render_template('donation_failed.html', donation_total=donation_total, balance=balance, new_balance=new_balance, meal_count=meal_count, snack_count=snack_count)


@app.route('/donation-success')
def donation_success():
    balance = request.args.get('balance',type=float)
    new_balance = float(balance) -  session['donation_total']
    donation_total = request.args.get('donation_total', 0, type=int)
    meal_count = request.args.get('meal_count', 0, type=int)
    snack_count = request.args.get('snack_count', 0, type=int)
    return render_template('donation_success.html', donation_total=donation_total, balance=balance, new_balance=new_balance, meal_count=meal_count, snack_count=snack_count)

@app.route('/donate/<username>/<student_id>/<balance>/<building>', methods=['GET', 'POST'])
def donate(username, student_id, balance, building):
    print("BALANCE " + balance)
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
            session['meal_count'] = 0
            session['snack_count'] = 0

        elif 'finish' in request.form:
            # check if user has enough first
            result = float(balance) - (session['donation_total'] + donation_amount)
            if(result < 1): # user isn't eligible to donate the amount they want
                return redirect(url_for('donation_failed', donation_total=session['donation_total'], meal_count=session['meal_count'],snack_count=session['snack_count'], balance=balance ))

            if session['donation_total'] + donation_amount > 50:
                error = "Donation limit reached. You cannot donate more than $50."     
                return render_template('donate.html', username=username, student_id=student_id, balance=balance,building=building,error=error)
            else:
                # valid donation amount 
                session['donation_total'] += donation_amount
                # with open bank_file


             #update the new balance

                
                return redirect(url_for('donation_success',donation_total=session['donation_total'],meal_count=session['meal_count'], snack_count=session['snack_count'],balance=balance))
    

    return render_template('donate.html', username=username, student_id=student_id, balance=balance,building=building)
 

@app.route('/request/<username>/<student_id>/<balance>/<building>',methods=['GET', 'POST'])
def request_page(username, student_id, balance, building):
    # check for the need of flexi 
    Toler_balance = 3010
    LME_balance = 2030

    Toler_balance_check = {
        "January": Toler_balance,
        "February": 2744,
        "March":2060,
        "April":1200,
        "May":521,
        "June":0,
        "July":0,
        "August":Toler_balance,
        "September":2744,
        "October": 2060,
        "Novemeber":1200,
        "December":521
    }

    LME_balance_check = {
        "January": LME_balance,
        "February": 1776,
        "March":1269,
        "April":762,
        "May":250,
        "June":0,
        "July":0,
        "August":LME_balance,
        "September":1776,
        "October": 1269,
        "Novemeber":762,
        "December":250
    }

    # Get current month
    current_month = datetime.now().strftime("%B")

    # Convert balance from string to float
    try:
        current_balance = float(balance)
    except ValueError:
        return f"Invalid balance format for student {student_id}."


     # Determine threshold and check eligibility
    if building == "Toler":
        threshold = Toler_balance_check.get(current_month, 0)
    elif building == "LME":
        threshold = LME_balance_check.get(current_month, 0)
    else:
        return f"Unknown building: {building}"

    # Check if student is eligible for request
    needs_flexi = current_balance < threshold
    
        #request meal/snack 

    #create a queue
    queue_file = 'queue.txt'
    success_message = None

    queue_file = 'queue.txt'
    success_message = None

    if request.method == 'POST' and needs_flexi:
        request_type = None
        amount = None
        success_message = None

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
        
        # Write to bank.txt
        with open('bank.txt', 'a') as f:
            f.write(f"{amount}\n")

        # Add user to queue.txt
        with open('queue.txt', 'a') as f:
            line = f"{username},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f.write(line)

        # Show success message
        success_message = f"✅ {username}, you’ve been added to the queue! You will be notified soon of your {request_type} status."
        queue_position = get_queue_position(username)

        return render_template(
            'typage.html',
            username=username,
            student_id=student_id,
            building=building,
            balance=current_balance,
            eligible=needs_flexi,
            queue_position=queue_position,
            amount=amount 
        )
    

    return render_template(
        'request.html',
        username=username,
        student_id=student_id,
        building=building,
        balance=current_balance,
        eligible=needs_flexi
    )


#add changes in the student balance


@app.route('/request/<username>/<student_id>/<building>/<balance>/<eligible>/<queue_position>/<amount>')
def typage(username, student_id, building, balance, eligible, queue_position, amount):
    balance = int(balance)
    queue_position = int(queue_position)
    amount = int(amount)

    # Read bank.txt entries
    with open('bank.txt', 'r') as f:
        bank_entries = [int(line.strip()) for line in f if line.strip()]

     # Count how many requests before the current one have the same amount
    # (i.e., competing for the same type of item: meal or snack)
    with open('queue.txt', 'r') as f:
        queue_lines = [line.strip() for line in f if line.strip()]
   
    # Get only those before this user in the queue
    prior_requests = queue_lines[:queue_position]

    # Count how many of them requested the same amount
    prior_same_amount = 0
    for line in prior_requests:
        user, timestamp = line.split(',', 1)
        # To make this simple, assume amount info is embedded somehow
        # If not, this won't work unless you have a second file that tracks request type
        # For now, we'll assume all users want the same amount
        prior_same_amount += 1

    # Count available items of this amount in the bank
    available_same_amount = bank_entries.count(amount)

    if prior_same_amount < available_same_amount:
        # Request can be fulfilled!
        balance += amount
        status = f"✅ Your request for ${amount} has been fulfilled!"
    else:
        # Request not available yet
        status = f"⏳ Your request for ${amount} is still pending. Please wait."

    return render_template('update.html',
        username=username,
        student_id=student_id,
        building=building,
        balance=balance
    )


@app.route('/update/<username>/<student_id>/<building>/<balance>')
def update(username, student_id, building, balance):
     

    return render_template('update.html',
                           username=username, 
                           student_id=student_id, 
                           building=building, 
                           balance=balance)

@app.route('/welcome/<username>')
def welcome(username):
    return render_template('welcome.html', username=username)


def get_queue_position(username):
    queue_file = 'queue.txt'
    queue_position = None
    #hello

    try:
        with open(queue_file, 'r') as f:
            queue_lines = f.readlines()

        # Loop through the queue lines and find the first occurrence of the username
        for position, line in enumerate(queue_lines, start=1):
            user, timestamp = line.strip().split(',')
            if user == username:
                queue_position = position
                break  # Once we find the username, we break out of the loop

        if queue_position is None:
            # If the username is not in the queue, assume they're in the first position
            queue_position = len(queue_lines) + 1

    except FileNotFoundError:
        queue_position = 1  # If the file doesn't exist, assume the first position

    return queue_position



# def send_email(username, subject, message_body):
#     sender_email = "cponti@dons.usfca.edu"
#     sender_password = "your_app_password"  # Use app password, not your real password
#     recipient_email = f"{username}@dons.usfca.edu"

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = subject

#     msg.attach(MIMEText(message_body, 'plain'))

#     try:
#         # Connect to Gmail SMTP server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, sender_password)

#         # Send the email
#         server.sendmail(sender_email, recipient_email, msg.as_string())
#         server.quit()
#         print("Email sent successfully to", recipient_email)
#         return True
#     except Exception as e:
#         print("Failed to send email:", e)
#         return False

if __name__ == '__main__':
    app.run(debug=True)