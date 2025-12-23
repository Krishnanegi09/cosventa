import tkinter as tk
from tkinter import messagebox
from admin import open_admin_login
from customer import open_customer_login, open_customer_register


# Main window
root = tk.Tk()
root.title("Cosventa : Cosmetic Store Management System")
root.geometry("500x400")
root.config(bg="#0b3d91")

# Title
title = tk.Label(
    root,
    text="Cosmetic Store Management System",
    font=("Helvetica", 16, "bold"),
    fg="white",
    bg="#0b3d91"
)
title.pack(pady=30)

# Button style
def styled_button(text, command):
    return tk.Button(
        root,
        text=text,
        command=command,
        font=("Helvetica", 12),
        width=20,
        bg="#3a3a3a",
        fg="black",
        activebackground="#555555",
        activeforeground="black",
        bd=0,
        pady=8
    )

# Button actions (temporary)
def admin_login():
    open_admin_login()

def customer_login():
    open_customer_login()

def customer_register():
    open_customer_register()

# Buttons
btn_admin = styled_button("Admin Login", admin_login)
btn_admin.pack(pady=10)

btn_customer = styled_button("Customer Login", customer_login)
btn_customer.pack(pady=10)

btn_register = styled_button("Customer Register", customer_register)
btn_register.pack(pady=10)

# Run app
root.mainloop()
