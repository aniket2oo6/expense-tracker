from flask import Flask, request, render_template, redirect
from database import get_connection
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    connection.close()
    return render_template('expenses.html', expenses = expenses)

@app.route('/add', methods = ['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        note = request.form['note']

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
            (amount, category, date, note)
        )
        connection.commit()
        connection.close()

        return redirect('/')

    return render_template('add.html')

@app.route('/reset', methods = ['POST'])
def reset_expenses():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM expenses')
    connection.commit()
    connection.close()

    return redirect('/')

@app.route('/dashboard')
def dashboard():
    connection = get_connection()
    df = pd.read_sql_query('SELECT * FROM expenses', connection)
    connection.close()

    if df.empty:
        return render_template('dashboard.html', no_data = True)

    category_totals = df.groupby('category')['amount'].sum()

    plt.figure(figsize = (6, 6))
    plt.pie(category_totals, labels = category_totals.index, autopct = '%1.1f%%')
    plt.title('Spending by Category')
    plt.savefig('static/chart.png')
    plt.close()

    return render_template('dashboard.html', no_data = False)

if __name__ == '__main__':
    app.run(debug = True)

