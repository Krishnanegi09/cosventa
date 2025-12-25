import mysql.connector as mysql

conn = mysql.connect(
    host="localhost",
    user="root",
    password="12345678"
)

cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS mydb")
cursor.execute("USE mydb")

# Create products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    product_price FLOAT,
    product_quantity INT
)
""")

# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    phone VARCHAR(15)
)
""")

# Create bills table
cursor.execute("""
CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    product_name VARCHAR(100),
    quantity INT,
    total_price FLOAT,
    bill_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

conn.commit()
conn.close()

print("Database and tables created successfully!")
