import mysql.connector as mysql
conn = mysql.connect(host="localhost", user="root", password="12345678", database="mydb")
def showmenu():
    while True:
        print("-"*136)
        print("-"*54,"Cosventa : A Cosmetic Store","-"*54)
        print("-"*136)
        print("\n")
        print("-"*65,"MENU","-"*65)
        print("\n")
        print("Press 1 to Add New Product")
        print("Press 2 to View All Products")
        print("Press 3 to Search Product by ID")
        print("Press 4 to Update Product by ID")
        print("Press 5 to Delete Product by ID")
        print("Press 6 to Purchase Products")
        print("Press 7 to Exit")
        print("_"*136)
        print("\n")
        
        choice = int(input("Enter your choice: "))
        if(choice==1):
            addproduct()
        elif(choice==2):
            viewproducts()
        elif(choice==3):
            searchproduct()
        elif(choice==4):
            updateproduct()
        elif(choice==5):
            deleteproduct()
        elif(choice==6):
            purchaseproducts()
        elif(choice==7):
            print("Exiting the program. Thank you!")
            break
        else:
            print("Invalid choice. Please try again.") 

def addproduct():
    product_id = int(input("Enter Product ID: "))
    product_name = input("Enter Product Name: ")
    product_price = float(input("Enter Product Price: "))
    product_quantity = int(input("Enter Product Quantity: "))
    cursor = conn.cursor()
    sql = "INSERT INTO products (product_id, product_name, product_price, product_quantity) VALUES (%s, %s, %s, %s)"
    val = (product_id, product_name, product_price, product_quantity)
    cursor.execute(sql, val)
    conn.commit()
    print(cursor.rowcount, "record inserted.")
    
    
def viewproducts():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    results = cursor.fetchall()
    print("Product ID | Product Name | Product Price | Product Quantity")
    for row in results:
        print(row[0], "| ", row[1], " | ", row[2], " | ", row[3]) 
        
    
def searchproduct():
    product_id = int(input("Enter Product ID to search: "))
    cursor = conn.cursor()
    sql = "SELECT * FROM products WHERE product_id = %s"
    val = (product_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        print("Product ID | Product Name | Product Price | Product Quantity")
        print(result[0], " | ", result[1], " | ", result[2], " | ", result[3])
    else:
        print("Product not found.")
        
        
def updateproduct():
    product_id = int(input("Enter Product ID to update: "))
    new_name = input("Enter new Product Name: ")
    new_price = float(input("Enter new Product Price: "))
    new_quantity = int(input("Enter new Product Quantity: "))
    cursor = conn.cursor()
    sql = "UPDATE products SET product_name = %s, product_price = %s, product_quantity = %s WHERE product_id = %s"
    val = (new_name, new_price, new_quantity, product_id)
    cursor.execute(sql, val)
    conn.commit()
    print(cursor.rowcount, "record(s) updated.")
    
    
def deleteproduct():
    product_id = int(input("Enter Product ID to delete: "))
    cursor = conn.cursor()
    sql = "DELETE FROM products WHERE product_id = %s"
    val = (product_id,)
    cursor.execute(sql, val)
    conn.commit()
    print(cursor.rowcount, "record(s) deleted.")
    
    
    
def purchaseproducts():
    cursor = conn.cursor()
    try:
        # Customer details
        cname = input("Enter Customer Name: ")
        phone = input("Enter Phone Number: ")

        cursor.execute(
            "INSERT INTO customers (customer_name, phone) VALUES (%s, %s)",
            (cname, phone)
        )
        conn.commit()
        customer_id = cursor.lastrowid

        # Product selection
        product_id = int(input("Enter Product ID to purchase: "))
        purchase_quantity = int(input("Enter quantity to purchase: "))

        cursor.execute(
            "SELECT product_quantity, product_price, product_name FROM products WHERE product_id = %s",
            (product_id,)
        )
        result = cursor.fetchone()

        if not result:
            print("Product not found.")
            return

        available_quantity, product_price, product_name = result

        if purchase_quantity > available_quantity:
            print("Insufficient stock available.")
            return

        total_price = product_price * purchase_quantity
        new_quantity = available_quantity - purchase_quantity

        # Update product quantity
        cursor.execute(
            "UPDATE products SET product_quantity = %s WHERE product_id = %s",
            (new_quantity, product_id)
        )

        # Insert into bills table (store product name here)
        cursor.execute(
            "INSERT INTO bills (customer_id, product_id, product_name, quantity, total_price) VALUES (%s, %s, %s, %s, %s)",
            (customer_id, product_id, product_name, purchase_quantity, total_price)
        )

        conn.commit()

        # Print bill
        print("\n----- BILL GENERATED -----")
        print("Customer:", cname)
        print("Phone:", phone)
        print("Product ID:", product_id)
        print("Product Name:", product_name)
        print("Quantity Purchased:", purchase_quantity)
        print("Total Amount: Rs.", total_price)

    except mysql.Error as err:
        conn.rollback()
        print("Database Error:", err)


        
        
showmenu()