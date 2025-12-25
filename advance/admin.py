import tkinter as tk
from tkinter import messagebox
from db import get_connection


class ModernEntry(tk.Frame):
    """Modern styled entry field"""
    def __init__(self, parent, label_text, is_password=False):
        super().__init__(parent, bg="#0f172a")
        
        label = tk.Label(
            self,
            text=label_text,
            font=("Arial", 14, "bold"),
            fg="#cbd5e1",
            bg="#0f172a",
            anchor=tk.W
        )
        label.pack(fill=tk.X, pady=(0, 8))
        
        self.entry = tk.Entry(
            self,
            font=("Arial", 14),
            bg="#1e293b",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=2,
            highlightbackground="#334155",
            highlightcolor="#2563eb",
            show="*" if is_password else ""
        )
        self.entry.pack(fill=tk.X, padx=0, pady=0, ipadx=15, ipady=12)
    
    def get(self):
        return self.entry.get()


class ModernButton(tk.Button):
    """Modern styled button"""
    def __init__(self, parent, text, command, bg_color="#2563eb", **kwargs):
        # Remove bg from kwargs if present to avoid conflicts
        kwargs.pop('bg', None)
        
        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Arial", 14, "bold"),
            bg=bg_color,
            fg="black",
            activebackground=bg_color,
            activeforeground="black",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            padx=30,
            pady=15,
            cursor="hand2",
            **kwargs
        )
        # Force background color after initialization
        self.configure(bg=bg_color)


def open_admin_login():
    win = tk.Toplevel()
    win.title("🔐 Admin Login - Cosventa")
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
        text="🔐",
        font=("Arial", 48),
        bg="#1e293b",
        fg="#2563eb"
    )
    icon_label.pack(pady=(20, 10))
    
    tk.Label(
        header_frame,
        text="ADMIN LOGIN",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack()

    # Content frame
    content_frame = tk.Frame(win, bg="#0f172a")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=40)

    # Username field
    username_field = ModernEntry(content_frame, "Username")
    username_field.pack(fill=tk.X, pady=20)

    # Password field
    password_field = ModernEntry(content_frame, "Password", is_password=True)
    password_field.pack(fill=tk.X, pady=20)

    # Login function
    def login():
        username = username_field.get()
        password = password_field.get()

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
            messagebox.showinfo("Success", "Login successful!")
            open_admin_panel()
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    # Login button
    login_btn = ModernButton(
        content_frame,
        "LOGIN",
        login,
        bg_color="#2563eb",
        width=22
    )
    login_btn.pack(pady=30)
    
    # Bind Enter key
    password_field.entry.bind("<Return>", lambda e: login())


def open_admin_panel():
    panel = tk.Toplevel()
    panel.title("⚙️ Admin Panel - Cosventa")
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
    header_frame = tk.Frame(panel, bg="#1e293b", height=100)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    tk.Label(
        header_frame,
        text="⚙️ ADMIN PANEL - PRODUCT MANAGEMENT",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=30)

    # Main container
    main_container = tk.Frame(panel, bg="#0f172a")
    main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

    # Left side - Input form
    form_frame = tk.Frame(main_container, bg="#1e293b", padx=30, pady=30, relief=tk.FLAT)
    form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
    
    tk.Label(
        form_frame,
        text="➕ ADD NEW PRODUCT",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1e293b"
    ).pack(pady=(0, 25))

    # Input Fields with modern styling
    fields = []
    field_names = ["Product Name", "Brand", "Price (₹)", "Quantity"]
    
    for field_name in field_names:
        field_frame = tk.Frame(form_frame, bg="#1e293b")
        field_frame.pack(fill=tk.X, pady=15)
        
        label = tk.Label(
            field_frame,
            text=field_name,
            font=("Arial", 14, "bold"),
            fg="#e2e8f0",
            bg="#1e293b",
            anchor=tk.W
        )
        label.pack(fill=tk.X, pady=(0, 8))
        
        entry = tk.Entry(
            field_frame,
            font=("Arial", 14),
            bg="#0f172a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=2,
            highlightbackground="#334155",
            highlightcolor="#2563eb"
        )
        entry.pack(fill=tk.X, ipadx=12, ipady=10)
        fields.append(entry)

    name_entry, brand_entry, price_entry, qty_entry = fields

    # Add Product function
    def add_product():
        name = name_entry.get().strip()
        brand = brand_entry.get().strip()
        price = price_entry.get().strip()
        qty = qty_entry.get().strip()

        if not (name and brand and price and qty):
            messagebox.showerror("Error", "All fields required")
            return
        
        try:
            price = float(price)
            qty = int(qty)
        except ValueError:
            messagebox.showerror("Error", "Invalid price or quantity")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (product_name, brand, price, quantity) VALUES (%s,%s,%s,%s)",
            (name, brand, price, qty)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product added successfully!")
        name_entry.delete(0, tk.END)
        brand_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        load_products()

    # Add Product button - Prominent and clear
    add_btn = ModernButton(
        form_frame,
        "➕ ADD PRODUCT TO INVENTORY",
        add_product,
        bg_color="#059669",
        width=25
    )
    add_btn.pack(pady=25)
    
    # Bind Enter key to add product (when quantity field is focused)
    qty_entry.bind("<Return>", lambda e: add_product())
    
    # Add separator for visual clarity
    separator = tk.Frame(form_frame, bg="#334155", height=2)
    separator.pack(fill=tk.X, pady=15)

    # Right side - Product list
    list_frame = tk.Frame(main_container, bg="#1e293b", padx=25, pady=25)
    list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    tk.Label(
        list_frame,
        text="📦 PRODUCT INVENTORY",
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
        selectbackground="#2563eb",
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
        cursor.execute("SELECT product_name, brand, price, quantity FROM products")
        products = cursor.fetchall()
        conn.close()
        
        if not products:
            listbox.insert(tk.END, "  No products available")
        else:
            for row in products:
                listbox.insert(tk.END, f"  {row[0]} | {row[1]} | ₹{row[2]} | Stock: {row[3]}")

    # Refresh button
    refresh_btn = ModernButton(
        list_frame,
        "🔄 REFRESH LIST",
        load_products,
        bg_color="#2563eb",
        width=22
    )
    refresh_btn.pack(pady=20)

    load_products()
