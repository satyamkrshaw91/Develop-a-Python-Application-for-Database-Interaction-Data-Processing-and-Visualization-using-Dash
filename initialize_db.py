import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    join_date DATE
)
''')

# Create transactions table
cursor.execute('''
CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    transaction_date DATE,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
)
''')

# Insert sample data into users table
users_data = [
    (1, 'Alice', 'alice@Gmail.com', '2024-01-01'),
    (2, 'Bob', 'bob@Gmail.com', '2024-02-15'),
    (3, 'Charlie', 'charlie@Gmail.com', '2024-03-20'),
    (4,'Satyam', 'satyam@Gmail.com', '2024-09-10')
]
cursor.executemany('''
INSERT INTO users (user_id, name, email, join_date)
VALUES (?, ?, ?, ?)
''', users_data)

# Insert sample data into transactions table
transactions_data = [
    (1, 1, 100.0, '2024-04-01'),
    (2, 1, 150.0, '2024-04-15'),
    (3, 2, 200.0, '2024-05-01'),
    (4,4,500.0,'2024-09-10')
]
cursor.executemany('''
INSERT INTO transactions (transaction_id, user_id, amount, transaction_date)
VALUES (?, ?, ?, ?)
''', transactions_data)

conn.commit()
conn.close()
