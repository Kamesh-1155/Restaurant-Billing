
# restaurant_app/order.py
from datetime import datetime
import random

class OrderManager:
    def __init__(self, menu_manager, db_manager):
        self.menu = menu_manager.menu
        self.db = db_manager

    def take_order(self):
        print("\nPlacing a new order...")
        customer_name = input("Customer name: ")
        items = []
        total = 0

        while True:
            code = input("Enter item code (or 'done' to finish): ")
            if code.lower() == 'done':
                break

            item = next((item for item in self.menu if item['code'] == code), None)
            if item:
                qty = int(input("Enter quantity: "))
                subtotal = float(item['price']) * qty
                items.append((item['name'], qty, subtotal))
                total += subtotal
            else:
                print("Item not found.")

        print("\n       --- Bill ---")
        for name, qty, subtotal in items:
            print(f"{name} x{qty} = ₹{subtotal:}")
        print(f" Total: ₹{total:}")

        self.db.insert_order(customer_name, items, total)
        print(" Order saved successfully.\n")
