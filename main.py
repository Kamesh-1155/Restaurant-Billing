# restaurant_app/main.py
from menu import MenuManager
from order import OrderManager
from db import DatabaseManager

def main():
    db = DatabaseManager()
    db.initialize()

    menu = MenuManager()
    order = OrderManager(menu, db)

    while True:
        print("""
======== Restaurant Management System ========
1. Add Menu Item
2. View Menu
3. Take Order
4. View Order History
5. Exit
=============================================
""")
        choice = input("Enter your choice: ")

        if choice == '1':
            menu.add_item()
        elif choice == '2':
            menu.view_menu()
        elif choice == '3':
            order.take_order()
        elif choice == '4':
            db.view_orders()
        elif choice == '5':
            print("Exiting... Thank you!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()