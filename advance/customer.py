import tkinter as tk
from tkinter import messagebox
from db import get_connection
from admin import ModernEntry, ModernButton


# ---------------- CUSTOMER REGISTRATION ----------------
def open_customer_register():
    win = tk.Toplevel()
    win.title("✨ Customer Registration - Cosventa")
    win.geometry("500x600")
    win.config(bg="#0f172a")
    win.resizable(False, False)
    
    # Center window
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

    # Header
    header_frame = tk.Frame(win, bg="#1e293b", height=150)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    icon_label = tk.Label(
        header_frame,
        text="✨",
        font=("Arial", 48),
        bg="#1e293b",
        fg="#d97706"
    )
    icon_label.pack(pady=(20, 10))
    
    tk.Label(
        header_frame,
        text="CREATE ACCOUNT",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack()

    # Content frame
    content_frame = tk.Frame(win, bg="#0f172a")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)

    # Form fields
    name_field = ModernEntry(content_frame, "Full Name")
    name_field.pack(fill=tk.X, pady=20)

    email_field = ModernEntry(content_frame, "Email")
    email_field.pack(fill=tk.X, pady=20)

    password_field = ModernEntry(content_frame, "Password", is_password=True)
    password_field.pack(fill=tk.X, pady=20)

    def register():
        name = name_field.get().strip()
        email = email_field.get().strip()
        password = password_field.get().strip()

        if not (name and email and password):
            messagebox.showerror("Error", "All fields required")
            return
        
        if "@" not in email:
            messagebox.showerror("Error", "Please enter a valid email")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO customers (name, email, password) VALUES (%s,%s,%s)",
                (name, email, password)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registration successful! Please login.")
            win.destroy()
        except Exception as e:
            if "Duplicate" in str(e) or "UNIQUE" in str(e):
                messagebox.showerror("Error", "Email already registered")
            else:
                messagebox.showerror("Error", "Registration failed")

    register_btn = ModernButton(
        content_frame,
        "✨ REGISTER",
        register,
        bg_color="#d97706",
        width=22
    )
    register_btn.pack(pady=30)
    
    # Bind Enter key
    password_field.entry.bind("<Return>", lambda e: register())


# ---------------- CUSTOMER LOGIN ----------------
def open_customer_login():
    win = tk.Toplevel()
    win.title("👤 Customer Login - Cosventa")
    win.geometry("500x600")
    win.config(bg="#0f172a")
    win.resizable(False, False)
    
    # Center window
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

    # Header
    header_frame = tk.Frame(win, bg="#1e293b", height=150)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    icon_label = tk.Label(
        header_frame,
        text="👤",
        font=("Arial", 48),
        bg="#1e293b",
        fg="#059669"
    )
    icon_label.pack(pady=(20, 10))
    
    tk.Label(
        header_frame,
        text="CUSTOMER LOGIN",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack()

    # Content frame
    content_frame = tk.Frame(win, bg="#0f172a")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)

    # Form fields
    email_field = ModernEntry(content_frame, "Email")
    email_field.pack(fill=tk.X, pady=20)

    password_field = ModernEntry(content_frame, "Password", is_password=True)
    password_field.pack(fill=tk.X, pady=20)

    def login():
        email = email_field.get().strip()
        password = password_field.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "All fields required")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM customers WHERE email=%s AND password=%s",
            (email, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Success", "Login successful!")
            open_customer_panel(result[1])
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    login_btn = ModernButton(
        content_frame,
        "LOGIN",
        login,
        bg_color="#059669",
        width=22
    )
    login_btn.pack(pady=30)
    
    # Bind Enter key
    password_field.entry.bind("<Return>", lambda e: login())


# ---------------- CUSTOMER PANEL ----------------
def open_customer_panel(customer_name):
    panel = tk.Toplevel()
    panel.title("🛒 Customer Panel - Cosventa")
    panel.geometry("1000x750")
    panel.config(bg="#0f172a")
    
    # Center window
    panel.update_idletasks()
    width = panel.winfo_width()
    height = panel.winfo_height()
    x = (panel.winfo_screenwidth() // 2) - (width // 2)
    y = (panel.winfo_screenheight() // 2) - (height // 2)
    panel.geometry(f"{width}x{height}+{x}+{y}")

    # Header
    header_frame = tk.Frame(panel, bg="#1e293b", height=120)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    welcome_label = tk.Label(
        header_frame,
        text=f"🛒 WELCOME, {customer_name.upper()}!",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#1e293b"
    )
    welcome_label.pack(pady=(25, 5))
    
    subtitle_label = tk.Label(
        header_frame,
        text="Browse and purchase your favorite cosmetics",
        font=("Arial", 14),
        fg="#94a3b8",
        bg="#1e293b"
    )
    subtitle_label.pack(pady=(0, 25))

    # Main container
    main_container = tk.Frame(panel, bg="#0f172a")
    main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

    # Left side - Product list
    list_frame = tk.Frame(main_container, bg="#1e293b", padx=25, pady=25)
    list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
    
    tk.Label(
        list_frame,
        text="💄 AVAILABLE PRODUCTS",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=(0, 20))

    # Scrollable listbox
    scroll_frame = tk.Frame(list_frame, bg="#1e293b")
    scroll_frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(scroll_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(
        scroll_frame,
        font=("Arial", 12),
        bg="#0f172a",
        fg="#ffffff",
        selectbackground="#059669",
        selectforeground="white",
        relief=tk.FLAT,
        bd=0,
        yscrollcommand=scrollbar.set,
        height=20
    )
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    def load_products():
        listbox.delete(0, tk.END)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT product_id, product_name, brand, price, quantity FROM products"
        )
        products = cursor.fetchall()
        conn.close()
        
        if not products:
            listbox.insert(tk.END, "  No products available")
        else:
            for row in products:
                stock_status = "✅ In Stock" if row[4] > 0 else "❌ Out of Stock"
                listbox.insert(
                    tk.END,
                    f"  {row[1]} | {row[2]} | ₹{row[3]} | {stock_status}"
                )

    # Right side - Purchase form
    purchase_frame = tk.Frame(main_container, bg="#1e293b", padx=30, pady=30)
    purchase_frame.pack(side=tk.RIGHT, fill=tk.Y)
    
    tk.Label(
        purchase_frame,
        text="🛍️ PURCHASE PRODUCT",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=(0, 25))

    # Quantity field
    qty_field = ModernEntry(purchase_frame, "Quantity to Buy")
    qty_field.pack(fill=tk.X, pady=20)

    def buy_product():
        if not listbox.curselection():
            messagebox.showerror("Error", "Please select a product")
            return

        try:
            qty = int(qty_field.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
            return

        selected = listbox.get(listbox.curselection())
        if "No products" in selected:
            messagebox.showerror("Error", "No products available")
            return
        
        data = selected.split(" | ")
        product_name = data[0].strip()
        brand = data[1].strip()
        price_str = data[2].strip().replace("₹", "")
        
        try:
            price = float(price_str)
        except:
            messagebox.showerror("Error", "Error reading product price")
            return

        # Get product details from database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT product_id, quantity FROM products WHERE product_name=%s AND brand=%s",
            (product_name, brand)
        )
        product = cursor.fetchone()
        
        if not product:
            messagebox.showerror("Error", "Product not found")
            conn.close()
            return
        
        product_id, stock = product

        if stock == 0:
            messagebox.showerror("Error", "Product is out of stock")
            conn.close()
            return

        if qty > stock:
            messagebox.showerror("Error", f"Insufficient stock. Available: {stock}")
            conn.close()
            return

        total = qty * price

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
            "✅ Purchase Successful!",
            f"Product: {product_name}\nBrand: {brand}\nQuantity: {qty}\nTotal: ₹{total:.2f}\n\nThank you for your purchase!",
            icon="info"
        )

        qty_field.entry.delete(0, tk.END)
        load_products()

    # Buy button
    buy_btn = ModernButton(
        purchase_frame,
        "🛒 BUY PRODUCT",
        buy_product,
        bg_color="#059669",
        width=22
    )
    buy_btn.pack(pady=20)
    
    # Refresh button
    refresh_btn = ModernButton(
        purchase_frame,
        "🔄 REFRESH PRODUCTS",
        load_products,
        bg_color="#2563eb",
        width=22
    )
    refresh_btn.pack(pady=15)
    
    # Bind Enter key
    qty_field.entry.bind("<Return>", lambda e: buy_product())

    load_products()
