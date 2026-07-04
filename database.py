import sqlite3

def get_connection():
    connection = sqlite3.connect('expenses.db')
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    """)
    connection.commit()
    connection.close()

if __name__ == '__main__':
    init_db()
    print('database initialized')

