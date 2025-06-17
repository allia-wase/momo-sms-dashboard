import sqlite3

def setup_database():
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE,
            type TEXT,
            amount INTEGER,
            sender TEXT,
            recipient TEXT,
            date DATETIME,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_transactions(transactions):
    conn = sqlite3.connect('momo.db')
    cursor = conn.cursor()
    for data in transactions:
        cursor.execute('''
            INSERT OR IGNORE INTO transactions 
            (transaction_id, type, amount, sender, recipient, date, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('transaction_id'),
            data.get('type'),
            data.get('amount'),
            data.get('sender'),
            data.get('recipient'),
            data.get('date'),
            data.get('description')
        ))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    from parse_sms import parse_sms_file
    transactions = parse_sms_file("data/sms.xml")
    setup_database()
    insert_transactions(transactions)
    print("Transactions inserted into database.")
