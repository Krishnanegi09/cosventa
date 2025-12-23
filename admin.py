import tkinter as tk
from tkinter import messagebox
from db import get_connection

def open_admin_login():
    win = tk.Toplevel()
    win.title("Admin Login")
    win.geometry("400x300")
    win.config(bg="#0b3d91")

    # Title
    tk.Label(
        win,
        text="Admin Login",
        font=("Helvetica", 14, "bold"),
        fg="white",
        bg="#0b3d91"
    ).pack(pady=20)

    # Username
    tk.Label(win, text="Username", fg="white", bg="#9a6969").pack()
    username_entry = tk.Entry(win)
    username_entry.pack(pady=5)

    # Password
    tk.Label(win, text="Password", fg="white", bg="#9a6969").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack(pady=5)

    # Login function
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login successful")
            open_admin_panel()
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    # Login button
    tk.Button(
        win,
        text="Login",
        command=login,
        bg="#3a3a3a",
        fg="black",
        width=15
    ).pack(pady=20)


def open_admin_panel():
    panel = tk.Toplevel()
    panel.title("Admin Panel")
    panel.geometry("600x500")
    panel.config(bg="#0b3d91")

    tk.Label(
        panel,
        text="Admin Panel - Product Management",
        font=("Helvetica", 14, "bold"),
        fg="white",
        bg="#0b3d91"
    ).pack(pady=15)

    # ---- Input Fields ----
    tk.Label(panel, text="Product Name", fg="white", bg="#0b3d91").pack()
    name_entry = tk.Entry(panel)
    name_entry.pack(pady=3)

    tk.Label(panel, text="Brand", fg="white", bg="#0b3d91").pack()
    brand_entry = tk.Entry(panel)
    brand_entry.pack(pady=3)

    tk.Label(panel, text="Price", fg="white", bg="#0b3d91").pack()
    price_entry = tk.Entry(panel)
    price_entry.pack(pady=3)

    tk.Label(panel, text="Quantity", fg="white", bg="#0b3d91").pack()
    qty_entry = tk.Entry(panel)
    qty_entry.pack(pady=3)

    # ---- Functions ----
    def add_product():
        name = name_entry.get()
        brand = brand_entry.get()
        price = price_entry.get()
        qty = qty_entry.get()

        if not (name and brand and price and qty):
            messagebox.showerror("Error", "All fields required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (product_name, brand, price, quantity) VALUES (%s,%s,%s,%s)",
            (name, brand, price, qty)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully")
        name_entry.delete(0, tk.END)
        brand_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        load_products()

    # ---- Product List ----
    listbox = tk.Listbox(panel, width=70)
    listbox.pack(pady=10)

    def load_products():
        listbox.delete(0, tk.END)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, brand, price, quantity FROM products")
        for row in cursor.fetchall():
            listbox.insert(tk.END, f"{row[0]} | {row[1]} | ₹{row[2]} | Qty: {row[3]}")
        conn.close()

    # ---- Buttons ----
    tk.Button(panel, text="Add Product", command=add_product,
              bg="#3a3a3a", fg="white", width=15).pack(pady=5)

    tk.Button(panel, text="Refresh List", command=load_products,
              bg="#3a3a3a", fg="white", width=15).pack(pady=5)

    load_products()
