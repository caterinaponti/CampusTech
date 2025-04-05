from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load balance.txt into memory (can optimize later with caching)
def load_student_data(student_id):
    with open("balance.txt", "r") as f:
        for line in f:
            parts = line.strip().split()
            if parts[0] == student_id:
                balance = float(parts[1])
                plan = parts[2]
                return balance, plan
    return None, None

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        balance, plan = load_student_data(student_id)
        if balance is None:
            flash("Invalid Student ID. Please try again.")
            return redirect(url_for("home"))
        
        chart_image = f"/static/{'lme_chart.png' if plan == 'LME' else 'toler_chart.png'}"
        lower_bound = 1200
        upper_bound = 2500

        return render_template(
            "student_action.html",
            student_id=student_id,
            balance=balance,
            plan=plan,
            chart_image=chart_image,
            lower_bound=lower_bound,
            upper_bound=upper_bound
        )
    
    return '''
        <form method="POST">
            <label for="student_id">Enter Student ID:</label><br>
            <input type="text" name="student_id" required><br>
            <button type="submit">Next</button>
        </form>
    '''

@app.route("/confirm", methods=["POST"])
def confirm_action():
    student_id = request.form.get("student_id")
    action = request.form.get("action")
    return f"Thanks, {student_id}. You chose to {action} a meal!"
