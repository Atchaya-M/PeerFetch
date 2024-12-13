from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import csv
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'



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

# LOG IN


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() 
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    conn.close()
    
    if user:
        session['user_email'] = email
        session['user_password'] = password
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 200

    

# SIGN UP

@app.route('/signup', methods=['POST'])
def signup_post():  
    data = request.json  
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Signup successful'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Email already exists'}), 409
    

@app.route('/myaccount')
def myaccount():
    user_email = session.get('user_email')
    return render_template('myaccount.html', user_email=user_email)


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

 
    conn = get_db_connection()
    conn.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, user_email))
    conn.commit()
    conn.close()

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

# ORDER PAGE
def load_items_from_csv():
    items = []
    with open('items.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row["Price"] = float(row["Price"][2:].strip())
            items.append(row)
    return items



@app.route('/order', methods=['GET', 'POST'])
def order():
    items = load_items_from_csv()  
    if request.method == 'POST':
        selected_items = request.json.get('selectedItems', [])
        total_price = request.json.get('totalPrice', 0.00)
        location = request.json.get('location', '')  
        comments = request.json.get('comments', '')
        order_details = request.json
        email = session.get('user_email')
       
        temp_order_details = []
        for i in order_details["selectedItems"]:
            if int(i["quantity"]) > 0:
                temp_order_details.append(i)
        order_details["selectedItems"] = temp_order_details
        order_id = save_order_to_db(order_details, email)

        session['selected_items'] = selected_items
        session['total_price'] = total_price
        session['order_id'] = order_id

    selected_items = session.get('selected_items', [])
    total_price = session.get('total_price', 0.00)
    return render_template('order.html', items=items, selected_items=selected_items, total_price=total_price)

def save_order_to_db(order_details, email):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (email, items, total_price, location, comments, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (email, str(order_details['selectedItems']), order_details['totalPrice'], order_details['location'], order_details['comments'], 'Pending'))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id


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

    cursor.execute("""
        SELECT * FROM orders 
        WHERE email = ? AND status == ?
    """, (session['user_email'], 'Pending'))
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
        
        cursor.execute("UPDATE orders SET status = 'Accepted' WHERE id = ?", (order_id,))
        
        conn.commit()

        cursor.execute("""
            SELECT email, items, total_price, location, comments, timestamp
            FROM orders
            WHERE id = ?
        """, (order_id,))

        order_data = cursor.fetchone()

        if not order_data:
            return jsonify({'success': False, 'error': 'Order not found.'})

        user_email = session.get('user_email')
        if not user_email:
            return jsonify({'success': False, 'error': 'User email not found in session.'})

        _, items, total_price, location, comments, timestamp = order_data

        cursor1.execute("""
            INSERT INTO delivery (order_id, email, items, total_price, location, comments, status, timestamp)
            VALUES (?,?, ?, ?, ?, ?, ?, ?)
        """, (order_id,user_email, items, total_price, location, comments, 'Accepted', timestamp))
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
    data = request.get_json()
    order_id = data.get("order_id")
    
    if not order_id:
        return jsonify({"success": False, "error": "Invalid order ID"})
    
    try:
        conn = sqlite3.connect("orders.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        
        if not order:
            return jsonify({"success": False, "error": "Order not found"})
        cursor.execute("""
            INSERT INTO orders (email, items, total_price, location, comments, status)
            VALUES (?, ?, ?, ?, ?,?)
        """, (order[1],order[2], order[3], order[4], order[5], "Pending"))
        
        conn.commit()
        conn.close()
        return jsonify({"success": True})
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

        cursor.execute("SELECT * FROM delivery WHERE email = ?", (user_email,))
        deliveries = cursor.fetchall()
        
        conn.close()
        return render_template("mydeliveries.html", deliveries=deliveries, user_email=user_email)
    
    except Exception as e:
        
        print(f"Error fetching deliveries: {e}")
        return render_template("error.html", message="Failed to load deliveries.")


# FORGOT PASSWORD

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/generate_and_update_password', methods=['POST'])
def generate_and_update_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400


    hashed_password = generate_random_password()

    try:

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()


        cursor.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (hashed_password, email)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Email not found"}), 404
        return jsonify({"new_password": hashed_password})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True)
