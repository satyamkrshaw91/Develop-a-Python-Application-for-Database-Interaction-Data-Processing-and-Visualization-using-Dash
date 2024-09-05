import sqlite3
import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Connect to the SQLite database
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Task 1: Retrieve users who joined within a specific date range
cursor.execute('''
SELECT * FROM users WHERE join_date BETWEEN '2024-01-01' AND '2024-09-31'
''')
users_in_date_range = cursor.fetchall()

# Task 2: Calculate the total amount spent by each user
cursor.execute('''
SELECT user_id, SUM(amount) as total_spent FROM transactions GROUP BY user_id
''')
total_spent_by_users = cursor.fetchall()

# Task 3: Generate a report showing each user’s name, email, and their total amount spent
cursor.execute('''
SELECT users.name, users.email, SUM(transactions.amount) as total_spent
FROM users
LEFT JOIN transactions ON users.user_id = transactions.user_id
GROUP BY users.user_id
''')
user_report = cursor.fetchall()

# Task 4: Find the top 3 users who spent the most
cursor.execute('''
SELECT users.name, SUM(transactions.amount) as total_spent
FROM users
JOIN transactions ON users.user_id = transactions.user_id
GROUP BY users.user_id
ORDER BY total_spent DESC
LIMIT 3
''')
top_3_users = cursor.fetchall()

# Task 5: Calculate the average transaction amount
cursor.execute('''
SELECT AVG(amount) FROM transactions
''')
avg_transaction_amount = cursor.fetchone()[0]

# Task 6: Identify users with no transactions
cursor.execute('''
SELECT name, email FROM users
WHERE user_id NOT IN (SELECT DISTINCT user_id FROM transactions)
''')
users_no_transactions = cursor.fetchall()

app = Dash(__name__)

app.layout = html.Div([
    html.H1("SQLite Database Interaction with Dash"),
    html.H2("Top 3 Users by Total Amount Spent"),
    dcc.Graph(id='bar-chart'),
    html.H2("Transaction Amounts Over Time"),
    dcc.Graph(id='line-chart'),
    html.H2("User Report"),
    html.Table(id='user-table'),
    html.H2("Users with No Transactions"),
    html.Table(id='no-transactions-table'),
])

# Graph 1: Bar chart showing the total amount spent by the top 3 users
@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-chart', 'id')
)
def update_bar_chart(_):
    df = pd.DataFrame(top_3_users, columns=['Name', 'Total Spent'])
    fig = px.bar(df, x='Name', y='Total Spent', title='Top 3 Users by Total Amount Spent')
    return fig

# Graph 2: Line chart of transaction amounts over time
@app.callback(
    Output('line-chart', 'figure'),
    Input('line-chart', 'id')
)

def update_line_chart(_):
    # Open a new connection inside the callback
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    # Perform the query
    cursor.execute('SELECT transaction_date, amount FROM transactions')
    df = pd.DataFrame(cursor.fetchall(), columns=['Date', 'Amount'])

    # Close the connection after the query
    conn.close()

    # Create the plot
    fig = px.line(df, x='Date', y='Amount', title='Transaction Amounts Over Time')
    return fig


# Table 1: User report
@app.callback(
    Output('user-table', 'children'),
    Input('user-table', 'id')
)
def update_user_table(_):
    rows = [html.Tr([html.Th("Name"), html.Th("Email"), html.Th("Total Spent")])]
    for row in user_report:
        rows.append(html.Tr([html.Td(row[0]), html.Td(row[1]), html.Td(row[2])]))
    return rows

# Table 2: Users with no transactions
@app.callback(
    Output('no-transactions-table', 'children'),
    Input('no-transactions-table', 'id')
)
def update_no_transactions_table(_):
    rows = [html.Tr([html.Th("Name"), html.Th("Email")])]
    for row in users_no_transactions:
        rows.append(html.Tr([html.Td(row[0]), html.Td(row[1])]))
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)
