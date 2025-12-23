import tkinter as tk
from tkinter import messagebox
from db import get_connection

# ---------------- CUSTOMER REGISTRATION ----------------
def open_customer_register():
    win = tk.Toplevel()
    win.title("Customer Registration")
    win.geometry("400x350")
    win.config(bg="#1e1e1e")

    tk.Label(win, text="Customer Registration",
             font=("Helvetica", 14, "bold"),
             fg="white", bg="#1e1e1e").pack(pady=20)

    tk.Label(win, text="Name", fg="white", bg="#1e1e1e").pack()
    name_entry = tk.Entry(win)
    name_entry.pack(pady=5)

    tk.Label(win, text="Email", fg="white", bg="#1e1e1e").pack()
    email_entry = tk.Entry(win)
    email_entry.pack(pady=5)

    tk.Label(win, text="Password", fg="white", bg="#1e1e1e").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

    def register():
        name = name_entry.get()
        email = email_entry.get()
        password = password_entry.get()

        if not (name and email and password):
            messagebox.showerror("Error", "All fields required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email, password) VALUES (%s,%s,%s)",
            (name, email, password)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Registration successful")
        win.destroy()

    tk.Button(win, text="Register", command=register,
              bg="#3a3a3a", fg="white", width=15).pack(pady=20)


# ---------------- CUSTOMER LOGIN ----------------
def open_customer_login():
    win = tk.Toplevel()
    win.title("Customer Login")
    win.geometry("400x300")
    win.config(bg="#1e1e1e")

    tk.Label(win, text="Customer Login",
             font=("Helvetica", 14, "bold"),
             fg="white", bg="#1e1e1e").pack(pady=20)

    tk.Label(win, text="Email", fg="white", bg="#1e1e1e").pack()
    email_entry = tk.Entry(win)
    email_entry.pack(pady=5)

    tk.Label(win, text="Password", fg="white", bg="#1e1e1e").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

    def login():
        email = email_entry.get()
        password = password_entry.get()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM customers WHERE email=%s AND password=%s",
            (email, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login successful")
            open_customer_panel(result[1])
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    tk.Button(win, text="Login", command=login,
              bg="#3a3a3a", fg="white", width=15).pack(pady=20)


# ---------------- CUSTOMER PANEL ----------------
def open_customer_panel(customer_name):
    panel = tk.Toplevel()
    panel.title("Customer Panel")
    panel.geometry("650x500")
    panel.config(bg="#1e1e1e")

    tk.Label(panel, text=f"Welcome, {customer_name}",
             font=("Helvetica", 14, "bold"),
             fg="white", bg="#1e1e1e").pack(pady=10)

    listbox = tk.Listbox(panel, width=80)
    listbox.pack(pady=10)

    tk.Label(panel, text="Quantity to Buy",
             fg="white", bg="#1e1e1e").pack()
    qty_entry = tk.Entry(panel)
    qty_entry.pack(pady=5)

    def load_products():
        listbox.delete(0, tk.END)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT product_id, product_name, brand, price, quantity FROM products"
        )
        for row in cursor.fetchall():
            listbox.insert(
                tk.END,
                f"{row[0]} | {row[1]} | {row[2]} | ₹{row[3]} | Stock: {row[4]}"
            )
        conn.close()

    def buy_product():
        if not listbox.curselection():
            messagebox.showerror("Error", "Select a product")
            return

        try:
            qty = int(qty_entry.get())
        except:
            messagebox.showerror("Error", "Enter valid quantity")
            return

        selected = listbox.get(listbox.curselection())
        data = selected.split(" | ")

        product_id = int(data[0])
        product_name = data[1]
        price = float(data[3].replace("₹", ""))
        stock = int(data[4].replace("Stock: ", ""))

        if qty > stock:
            messagebox.showerror("Error", "Insufficient stock")
            return

        total = qty * price

        conn = get_connection()
        cursor = conn.cursor()

        # Update stock
        cursor.execute(
            "UPDATE products SET quantity=quantity-%s WHERE product_id=%s",
            (qty, product_id)
        )

        # Insert sale record
        cursor.execute(
            "INSERT INTO sales (customer_name, product_name, quantity, total_price, sale_date) "
            "VALUES (%s,%s,%s,%s,NOW())",
            (customer_name, product_name, qty, total)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Bill",
            f"Product: {product_name}\nQuantity: {qty}\nTotal: ₹{total}"
        )

        qty_entry.delete(0, tk.END)
        load_products()

    tk.Button(panel, text="Buy Product", command=buy_product,
              bg="#3a3a3a", fg="white", width=15).pack(pady=10)

    load_products()
