from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data storage (replace this with a database in a real-world application)
users = {}
roles = {'admin', 'borrower', 'lender'}
transactions = []


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        role = request.form['role']
        users[email] = {'role': role, 'loans': []}
        return redirect(url_for('dashboard', email=email))
    return render_template('register.html', roles=roles)


@app.route('/dashboard/<email>')
def dashboard(email):
    user = users.get(email)
    if not user:
        return redirect(url_for('home'))

    role = user['role']
    loans = user['loans']

    return render_template('dashboard.html', email=email, role=role, loans=loans)


@app.route('/request_loan/<email>', methods=['POST'])
def request_loan(email):
    user = users.get(email)
    if not user or user['role'] != 'borrower':
        return redirect(url_for('home'))

    amount = request.form['amount']
    user['loans'].append({'amount': amount, 'status': 'Pending'})
    transactions.append({'email': email, 'action': 'Requested Loan'})

    return redirect(url_for('dashboard', email=email))


@app.route('/confirm_payment/<email>', methods=['POST'])
def confirm_payment(email):
    user = users.get(email)
    if not user or user['role'] != 'lender':
        return redirect(url_for('home'))

    loan_index = int(request.form['loan_index'])
    user['loans'][loan_index]['status'] = 'Paid'
    transactions.append({'email': email, 'action': 'Confirmed Payment'})

    return redirect(url_for('dashboard', email=email))


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html', transactions=transactions)


if __name__ == '__main__':
    app.run(debug=True)
