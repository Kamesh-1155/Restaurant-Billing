import streamlit as st
from menu import MenuManager
from db import DatabaseManager

# ---------- Initialization ----------
st.set_page_config(page_title="Restaurant Ordering System", layout="centered")

db = DatabaseManager()
db.initialize()

menu_manager = MenuManager()
menu = menu_manager.menu

# ---------- Title ----------
st.title("🍽 Restaurant Ordering System")

# ---------- Menu Display ----------
st.subheader("📋 Menu")

if not menu:
    st.warning("Menu is empty. Please add items.")
else:
    st.table(menu)

# ---------- Order Section ----------
st.subheader("🛒 Place Order")

customer_name = st.text_input("Customer Name")

selected_items = []
total_amount = 0.0

if menu:
    for item in menu:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"{item['name']} (₹{item['price']})")
        with col2:
            qty = st.number_input(
                f"Qty_{item['code']}",
                min_value=0,
                step=1,
                label_visibility="collapsed"
            )

        if qty > 0:
            subtotal = float(item['price']) * qty
            selected_items.append((item['name'], qty, subtotal))
            total_amount += subtotal

# ---------- Place Order ----------
if st.button("✅ Place Order"):
    if not customer_name:
        st.error("Please enter customer name.")
    elif not selected_items:
        st.error("Please select at least one item.")
    else:
        db.insert_order(customer_name, selected_items, total_amount)
        st.success("Order placed successfully!")

        st.subheader("🧾 Bill Summary")
        for name, qty, subtotal in selected_items:
            st.write(f"{name} × {qty} = ₹{subtotal:.2f}")

        st.write(f"### 💰 Total: ₹{total_amount:.2f}")

# ---------- Order History ----------
st.subheader("📦 Order History")

if st.button("View Order History"):
    db.cursor.execute("SELECT * FROM orders")
    orders = db.cursor.fetchall()

    if not orders:
        st.info("No orders found.")
    else:
        st.table(
            [{
                "Customer": o[1],
                "Items": o[2],
                "Total (₹)": f"{o[3]:.1f}",
                "Time": o[4]
            } for o in orders]
        )