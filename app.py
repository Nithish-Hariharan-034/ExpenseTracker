from flask import Flask, render_template, request, redirect
import sqlite3
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('expenses.db')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        notes = request.form['notes']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (date, category, amount, notes) VALUES (?, ?, ?, ?)',
                       (date, category, amount, notes))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_expense.html')
@app.route('/view', methods=['GET', 'POST'])
def view_expenses():
    expenses = []
    labels = []
    values = []
    total_amount = 0
    selected_month = datetime.now().month
    selected_year = datetime.now().year

    if request.method == 'POST':
        selected_month = int(request.form['month'])
        selected_year = int(request.form['year'])

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT date, category, amount FROM expenses')
        all_expenses = cursor.fetchall()
        conn.close()

        filtered_expenses = []
        category_totals = defaultdict(float)

        for date_str, category, amount in all_expenses:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            if date_obj.month == selected_month and date_obj.year == selected_year:
                filtered_expenses.append((date_str, category, amount))
                category_totals[category] += float(amount)
                total_amount += float(amount)

        expenses = filtered_expenses
        labels = list(category_totals.keys())
        values = list(category_totals.values())

    return render_template('view_expenses.html', expenses=expenses, labels=labels,
                           values=values, total_amount=total_amount,
                           selected_month=selected_month, selected_year=selected_year)


if __name__ == "__main__":
    app.run(debug=True)
