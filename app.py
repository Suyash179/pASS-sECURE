from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

# Check strength out of 5
def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    errors = [length_error, digit_error, uppercase_error, lowercase_error, symbol_error]
    strength = 5 - sum(errors)
    return strength

# Estimate how long it would take to crack the password
def estimate_crack_time(password):
    score = 0
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password): score += 1
    if re.search(r"[a-z]", password): score += 1
    if re.search(r"\d", password): score += 1
    if re.search(r"\W", password): score += 1

    if score >= 6:
        return "millions of years"
    elif score >= 5:
        return "years"
    elif score >= 4:
        return "months"
    elif score >= 3:
        return "days"
    elif score == 2:
        return "hours"
    else:
        return "seconds"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')
    strength = check_password_strength(password)
    crack_time = estimate_crack_time(password)

    if strength == 5:
        message = "Strong Password"
        color = "green"
    elif strength >= 3:
        message = "Moderate Password"
        color = "orange"
    else:
        message = "Weak Password"
        color = "red"

    return jsonify({
        'message': message,
        'color': color,
        'crack_time': crack_time
    })

if __name__ == '__main__':
    app.run(debug=True)
