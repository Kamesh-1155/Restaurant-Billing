# restaurant_app/db.py
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("restaurant.db")
        self.cursor = self.conn.cursor()

    def initialize(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                order_details TEXT,
                total REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def insert_order(self, customer_name, items, total):
        order_details = "; ".join([f"{name}x{qty}" for name, qty, _ in items])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO orders (customer_name, order_details, total, timestamp) VALUES (?, ?, ?, ?)",
                            (customer_name, order_details, total, timestamp))
        self.conn.commit()

    def view_orders(self):
        self.cursor.execute("SELECT * FROM orders")
        orders = self.cursor.fetchall()
        print("\n~~~~ Order History ~~~~")
        for order in orders:
            print(f"{order[0]}. {order[1]} | ₹{order[3]:.2f} | {order[4]} | {order[2]}")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~\n")
