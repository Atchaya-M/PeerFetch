from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit,send
import sqlite3
import csv
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")
users = {}  # Temporary storage for users, replace with database in production


def get_db_connection():
    conn = sqlite3.connect('users.db')  
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('signin.html') 

@app.route('/login')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html') 

@app.route('/chat/<orderId>/<role>')
def chat(orderId, role):
    return render_template('chat.html', order_id=orderId, role=role)

# Event for joining a room
@socketio.on('join')
def handle_join(data):
    order_id = data.get('order_id')  # Extract order_id
    role = data.get('role')          # Extract role
    join_room(order_id)  # Join room based on order ID
    send({'role': role , 'msg': 'Joined the room.'}, room=order_id)

# Event for sending a message
@socketio.on('send_message')
def handle_message(data):
    order_id = data.get('order_id')  # Extract order_id
    role = data.get('role')          # Extract role
    message = data.get('message')   # Extract message
    send({'role': role, 'msg': message}, room=order_id)

# Event for leaving a room
@socketio.on('leave')
def handle_leave(data):
    order_id = data.get('order_id')  # Extract order_id
    role = data.get('role')          # Extract role
    leave_room(order_id)  # Leave room based on order ID
    send({'role': role, 'msg': 'Left the room.'}, room=order_id)

DATABASE = 'users.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
     # Add reviews table
    c.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        name TEXT,
        comment TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')



    conn.commit()
    conn.close()

def create_orders_table():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            items TEXT NOT NULL,
            total_price REAL NOT NULL,
            location TEXT NOT NULL,
            comments TEXT,
            status TEXT DEFAULT 'Pending',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def create_delivery_table():
    conn = sqlite3.connect('delivery.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS delivery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            items TEXT NOT NULL,
            total_price REAL NOT NULL,
            location TEXT NOT NULL,
            comments TEXT,
            status TEXT DEFAULT 'Pending',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

create_orders_table()
create_delivery_table()
init_db()

def init_locations_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Create locations table
    c.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        college TEXT NOT NULL,
        location TEXT UNIQUE NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Run this function to create the locations table
init_locations_db()

def insert_locations():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    colleges = ["college1", "college2", "college3"]
    locations_per_college = 5

    # Insert unique locations for each college
    for college in colleges:
        for i in range(1, locations_per_college + 1):
            location_name = f"{college}-location{i}"
            try:
                c.execute("INSERT INTO locations (college, location) VALUES (?, ?)", (college, location_name))
            except sqlite3.IntegrityError:
                print(f"Location {location_name} already exists, skipping...")

    conn.commit()
    conn.close()

# Run this function to insert locations
insert_locations()

def add_column_if_not_exists(database, table, column, column_type):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    
    if column not in columns:
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
        print(f"Column '{column}' added to {table}.")
    else:
        print(f"Column '{column}' already exists in {table}.")
    
    conn.commit()
    conn.close()

def update_orders_table():
    add_column_if_not_exists('orders.db', 'orders', 'otp', 'TEXT')
    add_column_if_not_exists('orders.db', 'orders', 'college', 'TEXT')

def update_delivery_table():
    add_column_if_not_exists('delivery.db', 'delivery', 'otp', 'TEXT')
    add_column_if_not_exists('delivery.db', 'delivery', 'college', 'TEXT')

def update_users_table():
    add_column_if_not_exists(DATABASE, 'users', 'college', 'TEXT')

def update_reviews_table():
    add_column_if_not_exists(DATABASE, 'reviews', 'college', 'TEXT')

create_orders_table()
create_delivery_table()
init_db()
update_orders_table()
update_delivery_table()
update_users_table()
update_reviews_table()


def convert_otp_to_text():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect("delivery.db")
        cursor = conn.cursor()

        # Update the OTP column to ensure it is stored as a string
        cursor.execute("UPDATE delivery SET otp = CAST(otp AS TEXT)")

        # Commit the changes
        conn.commit()
        print("OTP column updated to store values as text successfully.")

    except sqlite3.Error as e:
        print(f"Error while updating OTP column: {e}")

    finally:
        # Close the database connection
        if conn:
            conn.close()

# Call the function
convert_otp_to_text()



# LOG IN


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() 
    email = data.get('email')
    password = data.get('password')
    college = data.get('college')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ? AND college = ?', (email, password, college)).fetchone()
    conn.close()
    
    if user:
        session['user_email'] = email
        session['user_password'] = password
        session['college'] = college
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 200

    

# SIGN UP

@app.route('/signup', methods=['POST'])
def signup_post():  
    data = request.json  
    print("Received Data:", data)
    email = data.get('email')
    password = data.get('password')
    college = data.get('college')

    # Validation checks
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        return jsonify({'success': False, 'message': 'Invalid email format'}), 400

    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(password_regex, password):
        return jsonify({
            'success': False,
            'message': 'Password must be at least 8 characters long, contain one digit, one special character, and one uppercase letter.'
        }), 400

    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (email, password, college) VALUES (?, ?, ?)', (email, password, college))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Signup successful'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Email already exists'}), 409

@app.route('/myaccount')
def myaccount():
    user_email = session.get('user_email')
    college = session.get('college')
    return render_template('myaccount.html', user_email=user_email, college=college)


# CHANGING PASSWORD

@app.route('/change-password', methods=['POST'])
def change_password():
    current_password = request.json.get('current_password')
    new_password = request.json.get('new_password')

    user_email = session.get('user_email')
    stored_password = session.get('user_password')

    if not user_email or not stored_password:
        return jsonify({'success': False, 'message': 'No user logged in'}), 400
    
    if current_password != stored_password:
        return jsonify({'success': False, 'message': 'Incorrect current password'}), 400

    # Password validation for the new password
    password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if not re.match(password_regex, new_password):
        return jsonify({
            'success': False,
            'message': 'New password must be at least 8 characters long, contain one digit, one special character, and one uppercase letter.'
        }), 400

    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, user_email))
    conn.commit()
    conn.close()

    # Update the password in the session
    session['user_password'] = new_password

    return jsonify({'success': True, 'message': 'Password changed successfully'}), 200


@app.route('/check-current-password', methods=['POST'])
def check_current_password():
    current_password = request.json.get('current_password')
    stored_password = session.get('user_password')
    if stored_password == current_password:
        return jsonify({'success': True, 'message': 'Current password is correct'}), 200
    else:
        return jsonify({'success': False, 'message': 'Incorrect current password'}), 400

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))

# LOADING THE CSV FILE FOR ORDER PAGE,RATINGS PAGE
def load_items_from_csv(user_college):
    items = []
    with open('items.csv', 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row["College"] == user_college:  # Filter by college
                row["Price"] = float(row["Price"][2:].strip())  # Convert price to float
                items.append(row)
    return items

# Ratings page
@app.route('/ratings')
def ratings():
    college = session.get('college')
    items = load_items_from_csv(college)
    return render_template('ratings.html', items=items)

# Submit review
@app.route('/submit_review', methods=['POST'])
def submit_review():
    college = session.get('college')
    item_name = request.form['item_name']
    rating = request.form['rating']
    name = request.form.get('name', 'Anonymous')
    comment = request.form.get('comment', '')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO reviews (item_name, rating, name, comment, college) VALUES (?, ?, ?, ?, ?)',
              (item_name, rating, name, comment, college))
    conn.commit()
    conn.close()

    return redirect(url_for('ratings'))

# Read reviews
@app.route('/read_reviews/<item_name>')
def read_reviews(item_name):
    college = session.get('college')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM reviews WHERE item_name = ? AND college = ?', (item_name,college))
    reviews = c.fetchall()
    conn.close()
    return render_template('review.html', item_name=item_name, reviews=reviews)
def generate_otp():
    return str(random.randint(100000, 999999))


@app.route('/order', methods=['GET', 'POST'])
def order():
    college = session.get('college')
    items = load_items_from_csv(college)  
    
    # Fetch locations for the specific college
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT location FROM locations WHERE college = ?', (college,))
    locations = [row[0] for row in cursor.fetchall()]
    conn.close()

    if request.method == 'POST':
        order_details = request.json
        selected_items = order_details.get('selectedItems', [])
        total_price = order_details.get('totalPrice', 0.00)
        location = order_details.get('location', '')  
        comments = order_details.get('comments', '')
        email = session.get('user_email')

        # Filter items with quantity > 0
        selected_items = [item for item in selected_items if int(item["quantity"]) > 0]
        order_details["selectedItems"] = selected_items
        
        if not selected_items:
            return {"success": False, "message": "No items selected."}, 400
        if location not in locations:
            return {"success": False, "message": "Invalid location selected."}, 400

        order_id, otp = save_order_to_db(order_details, email)

        session['selected_items'] = selected_items
        session['total_price'] = total_price
        session['order_id'] = order_id

        return {"success": True, "otp": otp}

    selected_items = session.get('selected_items', [])
    total_price = session.get('total_price', 0.00)

    return render_template('order.html', items=items, selected_items=selected_items, total_price=total_price, locations=locations)

def save_order_to_db(order_details, email):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    otp = generate_otp()
    college = session.get('college')
    cursor.execute('''
        INSERT INTO orders (email, items, total_price, location, comments, status, otp, college)
        VALUES (?, ?, ?, ?, ?, ?, ?,?)
    ''', (email, str(order_details['selectedItems']), order_details['totalPrice'], order_details['location'], order_details['comments'], 'Pending', otp, college))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id, otp


@app.route('/myorders')
def myorders_page():

    email = session.get('user_email')
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE email = ?', (email,))
    orders = cursor.fetchall()

    conn.close()
    return render_template('myorders.html', orders=orders)

# DELIVER

@app.route('/deliver')
def deliver_orders():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    college = session.get('college')
    cursor.execute("""
        SELECT * FROM orders 
        WHERE email != ? AND status == ? AND college = ?
    """, (session['user_email'], 'Pending', college))
    orders = cursor.fetchall()
    return render_template('deliver.html', orders=orders)


@app.route('/move_to_delivery', methods=['POST'])
def move_to_delivery():
    order_id = request.get_json().get('order_id')
    
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    conn1 = sqlite3.connect('delivery.db')
    cursor1 = conn1.cursor()
    
    try:
        # Update status in orders table
        cursor.execute("UPDATE orders SET status = 'Accepted' WHERE id = ?", (order_id,))
        conn.commit()

        # Fetch order details including OTP
        cursor.execute("""
            SELECT email, items, total_price, location, comments, timestamp, otp
            FROM orders
            WHERE id = ?
        """, (order_id,))

        order_data = cursor.fetchone()

        if not order_data:
            return jsonify({'success': False, 'error': 'Order not found.'})

        user_email = session.get('user_email')
        if not user_email:
            return jsonify({'success': False, 'error': 'User email not found in session.'})

        email, items, total_price, location, comments, timestamp, otp = order_data
        print("MOVING from order to delivery", otp)
        # Insert into delivery table
        cursor1.execute("""
            INSERT INTO delivery (order_id, email, items, total_price, location, comments, status, timestamp, otp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (order_id, user_email, items, total_price, location, comments, 'Accepted', timestamp, otp))
        conn1.commit()

        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        conn1.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        conn1.close()
        conn.close()


# REORDER
@app.route("/reorder", methods=["POST"])
def reorder():
    college = session.get('college')
    data = request.get_json()
    order_id = data.get("order_id")
    
    if not order_id:
        return jsonify({"success": False, "error": "Invalid order ID"})
    
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        
        # Fetch the original order details
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        
        if not order:
            return jsonify({"success": False, "error": "Order not found"})
        
        # Generate a new OTP
        otp = generate_otp()
        
        # Insert the new order with the generated OTP
        cursor.execute("""
            INSERT INTO orders (email, items, total_price, location, comments, status, otp, college)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (order[1], order[2], order[3], order[4], order[5], "Pending", otp, college))
        
        conn.commit()
        conn.close()
        # Respond with success and the new OTP
        return jsonify({"success": True, "otp": otp})
    except Exception as e:
        print("Error reordering:", e)
        return jsonify({"success": False, "error": "Database error"})

# MY DELIVERIES
@app.route("/mydeliveries")
def my_deliveries():
    user_email = session.get('user_email')
    
    if not user_email:
        return redirect(url_for('signin'))  
    
    try:
        conn = sqlite3.connect("delivery.db")
        cursor = conn.cursor()

        # Fetch deliveries
        cursor.execute("SELECT * FROM delivery WHERE email = ?", (user_email,))
        deliveries = cursor.fetchall()
        conn.close()
        # Debugging: Check fetched data
        return render_template("mydeliveries.html", deliveries=deliveries, user_email=user_email)
    
    except sqlite3.Error as db_error:
        print(f"Database Error: {db_error}")
        return render_template("error.html", message="Database error occurred.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return render_template("error.html", message="An unexpected error occurred.")

#OTP
@app.route("/update_status/<int:delivery_id>", methods=['POST'])
def update_status(delivery_id):
    try:
        conn = sqlite3.connect("delivery.db")
        cursor = conn.cursor()
        conn2 = sqlite3.connect("orders.db")
        cursor2 = conn2.cursor()

        # Fetch the current status, OTP, and order ID from the delivery table
        cursor.execute("SELECT status, otp, order_id FROM delivery WHERE id = ?", (delivery_id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'success': False, 'error': 'Delivery ID not found'}), 404

        current_status, stored_otp, order_id = result

        # Debugging logs
        print(f"Delivery ID: {delivery_id}, Current Status: {current_status}, Stored OTP: {stored_otp}")

        new_status = None

        if current_status == 'Accepted':
            new_status = 'Picked Up'
        elif current_status == 'Picked Up':
            otp = request.json.get('otp')  # Get OTP from request
            print(f"Received OTP: {otp}")  # Debugging log
            if otp and str(otp).strip() == str(stored_otp).strip():
                new_status = 'Delivered'
            else:
                return jsonify({'success': False, 'error': 'Invalid OTP'}), 400
        else:
            return jsonify({'success': False, 'error': 'Invalid status transition'}), 400

        # Update the delivery status
        cursor.execute("UPDATE delivery SET status = ? WHERE id = ?", (new_status, delivery_id))
        conn.commit()

        # Update the orders status
        cursor2.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn2.commit()

        # Debugging logs
        print(f"Order ID: {order_id}, New Status: {new_status}")

        # Close connections
        conn.close()
        conn2.close()

        return jsonify({'success': True, 'new_status': new_status})
    
    except Exception as e:
        print(f"Error updating status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500



# FORGOT PASSWORD

# Helper function to generate a random password
def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    temp_password = ''.join(random.choice(characters) for _ in range(length))
    return temp_password

# Function to send the temporary password to the user's email
def send_reset_email(user_email, temp_password):
    sender_email = SENDER_EMAIL
    sender_password = SENDER_PASSWORD  # Use an app password if 2-factor authentication is enabled
    receiver_email = user_email

    # Set up the email content
    subject = "Password Reset Request"
    body = f"Hello, \n\nYour temporary password is: {temp_password}\n\nPlease change your password as soon as possible."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Send the email using SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Route to handle "Forgot Password"
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if user:
        temp_password = generate_temp_password()
        
        # Send the reset email
        email_sent = send_reset_email(email, temp_password)
        if email_sent:
            # Update the database with the temporary password
            conn = get_db_connection()
            conn.execute('UPDATE users SET password = ? WHERE email = ?', (temp_password, email))
            conn.commit()
            conn.close()

            return jsonify({'success': True, 'message': 'Temporary password has been sent to your email'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to send email'}), 500
    else:
        return jsonify({'success': False, 'message': 'Email not found'}), 404

if __name__ == "__main__":
    socketio.run(app, debug=True)
