# restaurant_app/backend.py
from menu import MenuManager
from order import OrderManager
from db import DatabaseManager

# Initialize restaurant system
db = DatabaseManager()
db.initialize()
menu = MenuManager()
order = OrderManager(menu, db)

# Conversation state
conversation_state = {
    "step": None,
    "customer_name": None,
    "items": []
}

def handle_message(user_message: str) -> str:
    """Main chatbot logic."""
    global conversation_state
    step = conversation_state["step"]

    # Start order process
    if "order" in user_message.lower() and step is None:
        conversation_state["step"] = "name"
        return "🍽️ Great! Let’s start your order. What’s your name?"

    # Step 1: Get customer name
    if step == "name":
        conversation_state["customer_name"] = user_message
        conversation_state["step"] = "item"
        return f"Thanks {user_message}! Please enter the item code you want to order. Type 'menu' to see options."

    # Step 2: Get item code
    if step == "item":
        if user_message.lower() == "done":
            if conversation_state["items"]:
                conversation_state["step"] = "confirm"
                return "✅ Do you want to confirm your order? (yes/no)"
            else:
                return "⚠️ You haven’t added any items. Please enter an item code."

        if user_message.lower() == "menu":
            return "\n".join([f"{item['code']} - {item['name']} - ₹{item['price']}" for item in menu.menu])

        item = next((i for i in menu.menu if i['code'] == user_message), None)
        if item:
            conversation_state["current_item"] = item
            conversation_state["step"] = "qty"
            return f"How many {item['name']} would you like?"
        else:
            return "❌ Item code not found. Please try again or type 'menu'."

    # Step 3: Get quantity
    if step == "qty":
        try:
            qty = int(user_message)
            item = conversation_state["current_item"]
            subtotal = float(item['price']) * qty
            conversation_state["items"].append((item['name'], qty, subtotal))
            conversation_state["step"] = "item"
            return f"Added {item['name']} x{qty} = ₹{subtotal:.2f}. Enter another item code or type 'done'."
        except ValueError:
            return "⚠️ Please enter a valid number for quantity."

    # Step 4: Confirm order
    if step == "confirm":
        if user_message.lower() == "yes":
            total = sum(sub for _, _, sub in conversation_state["items"])
            order.db.insert_order(conversation_state["customer_name"], conversation_state["items"], total)
            conversation_state = {"step": None, "customer_name": None, "items": []}  # Reset
            return f"🎉 Order placed successfully! Your total is ₹{total:.2f}."
        else:
            conversation_state = {"step": None, "customer_name": None, "items": []}  # Reset
            return "❌ Order cancelled."

    # Other commands
    if "menu" in user_message.lower():
        return "\n".join([f"{item['code']} - {item['name']} - ₹{item['price']}" for item in menu.menu])

    if "history" in user_message.lower():
        orders = db.cursor.execute("SELECT * FROM orders").fetchall()
        return "\n".join([f"{o[1]} | ₹{o[3]} | {o[4]} | {o[2]}" for o in orders]) or "No orders yet."

    if user_message.lower() in ["hi", "hello"]:
        return "👋 Hello! You can say 'menu', 'order', or 'history'."

    if user_message.lower() in ["exit", "bye"]:
        return "👋 Goodbye! Have a nice day 🍽️"

    return "🤖 Sorry, I didn’t understand. Try: menu, order, history, exit."
