import sqlite3

# Connect to the database
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Update the status to 'Delivered' for the order with id 44
cursor.execute("UPDATE orders SET status = ? WHERE id = ?", ('Delivered', 44))

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Order status updated to 'Delivered' for id 44.")

