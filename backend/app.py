from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('momo.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM transactions')
    rows = cur.fetchall()
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(debug=True)
