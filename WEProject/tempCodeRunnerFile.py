import sqlite3

# Connect to the orders database
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Check the schema of the orders table
cursor.execute("PRAGMA table_info(orders);")
columns = cursor.fetchall()

# Print the columns and their details
print("Orders Table Schema:")
for column in columns:
    print(column)

# Check the contents of the orders table
cursor.execute("SELECT * FROM orders;")
rows = cursor.fetchall()

# Print all rows in the orders table
print("\nOrders Table Contents:")
for row in rows:
    print(row)

# Close the connection
conn.close()
