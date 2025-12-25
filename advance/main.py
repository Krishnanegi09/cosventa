import tkinter as tk
from tkinter import messagebox
from admin import open_admin_login
from customer import open_customer_login, open_customer_register


class ModernButton(tk.Button):
    """Modern styled button"""
    def __init__(self, parent, text, command, bg_color="#2563eb", **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Arial", 16, "bold"),
            bg=bg_color,
            fg="black",
            activebackground=bg_color,
            activeforeground="black",
            relief=tk.FLAT,
            bd=0,
            padx=40,
            pady=20,
            cursor="hand2",
            **kwargs
        )


# Main window
root = tk.Tk()
root.title("✨ Cosventa - Cosmetic Store Management System")
root.geometry("700x750")
root.config(bg="#0f172a")

# Center window
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

# Header frame
header_frame = tk.Frame(root, bg="#1e293b", height=220)
header_frame.pack(fill=tk.X)
header_frame.pack_propagate(False)

# Logo/Icon area
icon_label = tk.Label(
    header_frame,
    text="💄",
    font=("Arial", 64),
    bg="#1e293b",
    fg="#fbbf24"
)
icon_label.pack(pady=(30, 10))

# Title
title = tk.Label(
    header_frame,
    text="COSVENTA",
    font=("Arial", 42, "bold"),
    fg="#ffffff",
    bg="#1e293b"
)
title.pack()

subtitle = tk.Label(
    header_frame,
    text="Cosmetic Store Management System",
    font=("Arial", 16),
    fg="#94a3b8",
    bg="#1e293b"
)
subtitle.pack(pady=(8, 20))

# Main content frame
content_frame = tk.Frame(root, bg="#0f172a")
content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

# Welcome text
welcome_label = tk.Label(
    content_frame,
    text="Welcome! Choose your access level",
    font=("Arial", 18),
    fg="#e2e8f0",
    bg="#0f172a"
)
welcome_label.pack(pady=(0, 40))

# Button container with better spacing
button_frame = tk.Frame(content_frame, bg="#0f172a")
button_frame.pack(fill=tk.BOTH, expand=True)

# Button actions
def admin_login():
    open_admin_login()

def customer_login():
    open_customer_login()

def customer_register():
    open_customer_register()

# Styled buttons with professional colors
btn_admin = ModernButton(
    button_frame,
    "🔐 ADMIN LOGIN",
    admin_login,
    bg_color="#2563eb",
    width=28
)
btn_admin.pack(pady=15)

btn_customer = ModernButton(
    button_frame,
    "👤 CUSTOMER LOGIN",
    customer_login,
    bg_color="#059669",
    width=28
)
btn_customer.pack(pady=15)

btn_register = ModernButton(
    button_frame,
    "👥 CUSTOMER REGISTER",
    customer_register,
    bg_color="#d97706",
    width=28
)
btn_register.pack(pady=15)

# Footer
footer_label = tk.Label(
    content_frame,
    text="© 2025 Cosventa. All rights reserved.",
    font=("Arial", 11),
    fg="#64748b",
    bg="#0f172a"
)
footer_label.pack(side=tk.BOTTOM, pady=(40, 0))

# Run app
root.mainloop()
