# Flask API for a reservation system
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
import random
import hashlib
import timestamp
import datetime
import os
import json
# Import tests.py
import tests


### Configure Flask app ###

# Define default flask configurations
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Set flask secret key as urandom string
app.config['SECRET_KEY'] = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

# Define other configurations
database_path = './Data/database.db'
config_path = 'Data/configs.json'

### Helpers ###

# Define database connection and cursor
def connect_db():
    return sqlite3.connect(database_path)
def db_cursor():
    return connect_db().cursor()

# Create two tables: users, reservations, and items
def initialize_db():
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        email TEXT NOT NULL,
        permissions TEXT NOT NULL
    )''')
    db_cur.execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        item TEXT NOT NULL,
        status TEXT NOT NULL
    )''')
    db_cur.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL
    )''')
    # Commit changes to database
    db.commit()
    db.close()


### Utility functions ###

# Get hash from a password and salt
def get_hash(password, salt):
    # Hash password
    hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Return hash
    return hash.hex()

# Convert readable time to timestamp
def readable_to_timestamp(readable_time):
    # Convert readable time to datetime object
    readable_time = datetime.datetime.strptime(readable_time, '%Y-%m-%d %H:%M:%S')
    # Convert datetime object to timestamp
    timestamp = int(readable_time.timestamp())
    # Return timestamp
    return int(timestamp)

### BACKEND ###
def get_reservation(reservation_id):
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Get reservation from database
    reservation = db_cur.execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,)).fetchone()
    # Close db connection
    db.close()
    # Return reservation
    return reservation

def user_exists(username):
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Check if username exists
    user = db_cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    # Close db connection
    db.close()
    # Return True if user exists
    return user is not None

def item_exists(item_name):
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Check if item exists
    item = db_cur.execute('SELECT * FROM items WHERE name = ?', (item_name,)).fetchone()
    # Close db connection
    db.close()
    # Return True if item exists
    return item is not None

### USER FUNCTIONS ###

# Authenticate users
def authenticate(username, password):
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Check if username exists
    user = db_cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None:
        # Close db connection
        db.close()
        return False
    # Get hash and salt from database
    hash_salt = db_cur.execute('SELECT hash, salt FROM users WHERE username = ?', (username,)).fetchone()
    # Check if password is valid
    if hash_salt[0] != get_hash(password, hash_salt[1]):
        # Close db connection
        db.close()
        return False
    # Return True if user is authenticated
    db.close()
    return True

# Handle login request
@app.route('/login', methods=['POST'])
def login():
    try:
        # Define db and db_cur
        db = connect_db()
        db_cur = db.cursor()
        # Get username and password from request
        username = request.form['username']
        password = request.form['password']
        # Check if username exists
        user = db_cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user is None:
            return jsonify({'status': 'error', 'error': 'Authentication failed'})
        # Authenticate user
        if not authenticate(username, password):
            return jsonify({'status': 'error', 'error': 'Authentication failed'})
        # Close database connection
        db.close()
        # Return user info
        return jsonify({'status': 'success', 'username': user[1], 'permissions': user[5]})
    except Exception as e:
        # Print error
        print(e)
        # Return error
        return jsonify({'status': 'error', 'error': 'Internal server error'})

# Get list of items without reservations between given times -- tested
@app.route('/items', methods=['POST'])
def get_items():
    try:
        # Define db and db_cur
        db = connect_db()
        db_cur = db.cursor()
        # Get start and end times from request
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        # Run tests on start and end times
        if not tests.check_time_valid(start_time) or not tests.check_time_valid(end_time):
            return jsonify({'status': 'error', 'error': 'Invalid time'})
        # Convert start and end times to timestamps
        start_time = readable_to_timestamp(start_time)
        end_time = readable_to_timestamp(end_time)
        # Get list of items from database
        items = db_cur.execute('SELECT * FROM items').fetchall()
        # Close database connection
        db.close()
        # Check list of items for reservations between given times
        for item in items:
            # Define db and db_cur
            db = connect_db()
            db_cur = db.cursor()
            # Get list of reservations for item where start time is before end time and end time is after start time
            within_reservations = db_cur.execute('SELECT * FROM reservations WHERE item = ? AND start_time <= ? AND end_time >= ?', (item[1], end_time, start_time)).fetchall()
            # Get list of reservations where start time is before start time and end time is after end time
            encap_reservations = db_cur.execute('SELECT * FROM reservations WHERE item = ? AND start_time <= ? AND end_time >= ?', (item[1], start_time, start_time)).fetchall()
            # Close database connection
            db.close()
            # If there are existing reservations, remove item from list
            if len(within_reservations) > 0:
                items.remove(item)
            # If there are existing reservations, remove item from list
            elif len(encap_reservations) > 0:
                items.remove(item)
        # Create field names for items
        field_names = ['id', 'name', 'description', 'status']
        # Create list of items with field names
        items = [dict(zip(field_names, item)) for item in items]
        # Return list of items
        return jsonify(items)
    except Exception as e:
        # Debug print
        print(e)
        # Return error
        return jsonify({'status': 'error', 'error': 'Internal server error'})

# Handle reservation request
@app.route('/reserve', methods=['POST'])
def reserve():
    error = None
    try:
        ## Getting forms ##
        username = request.form['username']
        password = request.form['password']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        item = request.form['item']
        ## Authentication ##
        if not authenticate(username, password):
            error = 'Authentication failed'
        ## Error checking ##
        if not item_exists(item):
            error = 'Item not found'
        if readable_to_timestamp(start_time) > readable_to_timestamp(end_time):
            error = 'Start time is after end time'
        if readable_to_timestamp(start_time) < datetime.datetime.now().timestamp():
            error = 'Start time is before current time'
        if readable_to_timestamp(end_time) < datetime.datetime.now().timestamp():
            error = 'End time is before current time'
        db = connect_db()
        db_cur = db.cursor()
        # Get reservations for item where start time is before end time and end time is after start time
        reservations = db_cur.execute('SELECT * FROM reservations WHERE item = ? AND start_time <= ? AND end_time >= ?', (item, end_time, start_time)).fetchall()
        # Get reservations where start time is before start time and end time is after end time
        encap_reservations = db_cur.execute('SELECT * FROM reservations WHERE item = ? AND start_time <= ? AND end_time >= ?', (item, start_time, start_time)).fetchall()
        db.close()
        # If there are existing reservations, error
        if len(reservations) > 0:
            error = 'Item is reserved'
        elif len(encap_reservations) > 0:
            error = 'Item is reserved'
        if error is None:
            ## Create reservation ##
            db = connect_db()
            db_cur = db.cursor()
            # Insert reservation into database
            db_cur.execute('INSERT INTO reservations (username, item, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)', (username, item, readable_to_timestamp(start_time), readable_to_timestamp(end_time), 'pending'))
            # Close database connection
            db.commit()
            db.close()
            return jsonify({'status': 'success'})
        else:
            # Debug print
            print(error)
            return jsonify({'status': 'error', 'error': error})
    except:
        print('Error')
        return jsonify({'status': 'error', 'error': 'Internal server error'})

# Cancel reservation
@app.route('/cancel', methods=['POST'])
def cancel():
    # Get username, password, and reservation id from request
    username = request.form['username']
    password = request.form['password']
    reservation_id = request.form['reservation_id']
    # Authenticate user
    if not authenticate(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Check if reservation exists
    reservation = get_reservation(reservation_id)
    if reservation is None:
        return jsonify({'error': 'Reservation not found'})
    # Check if username for reservation is correct
    if reservation[0] != username:
        return jsonify({'error': 'Username is incorrect'})
    # Check if reservation is pending
    if reservation[4] != 'pending':
        return jsonify({'error': 'Reservation is not pending'})
    # Cancel reservation
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
    db.commit()
    db.close()
    # Return reservation info
    return jsonify({'username': username, 'item': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'cancelled'})

### END USER FUNCTIONS ###


### Admin functions ###

# Authenticate and check if user is admin
def authenticate_admin(username, password):
    # Check if username exists
    if not user_exists(username):
        # Close database connection
        db.close()
        return False
    # Get hash and salt from database
    db = connect_db()
    db_cur = db.cursor()
    hash_and_salt = db_cur.execute('SELECT hash, salt FROM users WHERE username = ?', (username,)).fetchone()
    # Close database connection
    db.close()
    # Check if password is correct
    if hash_and_salt is not None:
        if hash_and_salt[0] == get_hash(password, hash_and_salt[1]):
            return True
        else:
            return False
    else:
        return False

# lend reservation (Only admin can lend)
@app.route('/admin/lend', methods=['POST'])
def lend():
    # Get username, password, and reservation id from request
    username = request.form['username']
    password = request.form['password']
    reservation_id = request.form['reservation_id']
    # Authenticate admin
    if not authenticate_admin(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Check if reservation exists
    reservation = get_reservation(reservation_id)
    if reservation is None:
        return jsonify({'error': 'Reservation not found'})
    # Check if username for reservation is correct
    if reservation[0] != username:
        return jsonify({'error': 'Username is incorrect'})
    # Check if reservation is pending
    if reservation[4] != 'pending':
        return jsonify({'error': 'Reservation is not pending'})
    # lend reservation
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('UPDATE reservations SET status = ? WHERE id = ?', ('lended', reservation_id))
    db.commit()
    db.close()
    # Return reservation info
    return jsonify({'username': username, 'item': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'lent'})

# return reservation (Only admin can return)
@app.route('/admin/return', methods=['POST'])
def return_reservation():
    # Get username, password, and reservation id from request
    username = request.form['username']
    password = request.form['password']
    reservation_id = request.form['reservation_id']
    # Authenticate user
    if not authenticate_admin(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Check if reservation exists
    reservation = get_reservation(reservation_id)
    if reservation is None:
        return jsonify({'error': 'Reservation not found'})
    # Check if username for reservation is correct
    if reservation[0] != username:
        return jsonify({'error': 'Username is incorrect'})
    # Check if reservation is lent
    if reservation[4] != 'lent':
        return jsonify({'error': 'Reservation is not lent'})
    # Return reservation
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('UPDATE reservations SET status = ? WHERE id = ?', ('returned', reservation_id))
    db.commit()
    db.close()
    # Return reservation info
    return jsonify({'username': username, 'item': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'returned'})

# Get overdue reservations (Only admin can get overdue reservations)
@app.route('/admin/overdue', methods=['POST'])
def get_overdue_reservations():
    # Get username and password from request
    username = request.form['username']
    password = request.form['password']
    # Authenticate user
    if not authenticate_admin(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Get overdue reservations
    db = connect_db()
    db_cur = db.cursor()
    reservations = db_cur.execute('SELECT * FROM reservations WHERE status = ?', ('lended',)).fetchall()
    db.close()
    # Check current time
    current_time = datetime.now()
    # Check if reservation is overdue
    overdue_reservations = []
    for reservation in reservations:
        if reservation[3] < current_time:
            overdue_reservations.append(reservation)
    # Return overdue reservations
    return jsonify({'overdue_reservations': overdue_reservations})

# Get pending reservations beyond start time (Only admin can get pending reservations)
@app.route('/admin/pending', methods=['POST'])
def get_pending_reservations():
    # Get username and password from request
    username = request.form['username']
    password = request.form['password']
    # Authenticate user
    if not authenticate_admin(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Get pending reservations
    db = connect_db()
    db_cur = db.cursor()
    reservations = db_cur.execute('SELECT * FROM reservations WHERE status = ?', ('pending',)).fetchall()
    db.close()
    # Check current time
    current_time = datetime.now()
    # Check if reservation is pending
    pending_reservations = []
    for reservation in reservations:
        if reservation[3] > current_time:
            pending_reservations.append(reservation)
    # Return pending reservations
    return jsonify({'pending_reservations': pending_reservations})

# List all users (Only admin can list users)
@app.route('/admin/users', methods=['POST'])
def list_users():
    # Get username and password from request
    username = request.form['username']
    password = request.form['password']
    # Authenticate user
    if not authenticate_admin(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Get all users
    db = connect_db()
    db_cur = db.cursor()
    users = db_cur.execute('SELECT * FROM users').fetchall()
    db.close()
    # Convert users to list of dictionaries
    users_list = []
    for user in users:
        users_list.append({'username': user[1], 'permissions': user[5]})
    db.close()
    # Return all users and their details
    return jsonify({'users': users_list})

# Handle register request (Only for admin)
@app.route('/admin/register', methods=['POST'])
def register():
    # Authenticate admin
    if not authenticate_admin(request.form['username'], request.form['password']):
        return jsonify({'error': 'Authentication failed'})
    # Get new username, password, email, and permissions from request
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    new_email = request.form['new_email']
    new_permissions = request.form['new_permissions']
    # Generate salt in bytes
    new_salt = os.urandom(16)
    # Generate hash from password and salt
    new_hash = get_hash(new_password, new_salt)
    # Check if user already exists
    if user_exists(new_username):
        return jsonify({'error': 'User already exists'})
    # Insert new user into database
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('INSERT INTO users (username, hash, salt, email, permissions) VALUES (?, ?, ?, ?, ?)', (new_username, new_hash, new_salt, new_email, new_permissions))
    db.commit()
    db.close()
    # Return new user info
    return jsonify({'username': new_username, 'permissions': new_permissions})

# Add new item (Only admin can add new item)
@app.route('/admin/add_item', methods=['POST'])
def add_item():
    # Authenticate admin
    if not authenticate_admin(request.form['username'], request.form['password']):
        return jsonify({'error': 'Authentication failed'})
    # Get new item name and description from request
    new_item_name = request.form['new_item_name']
    new_item_description = request.form['new_item_description']
    # Check if item name already used
    if item_exists(new_item_name):
        return jsonify({'error': 'item already exists'})
    # Insert new item into database with status 'available'
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('INSERT INTO items (name, description, status) VALUES (?, ?, ?)', (new_item_name, new_item_description, 'available'))
    db.commit()
    db.close()
    # Return new item info
    return jsonify({'item_name': new_item_name, 'item_description': new_item_description, 'item_status': 'available'})

# Remove item (Only admin can remove item)
@app.route('/admin/remove_item', methods=['POST'])
def remove_item():
    # Authenticate admin
    if not authenticate_admin(request.form['username'], request.form['password']):
        return jsonify({'error': 'Authentication failed'})
    # Get item name from request
    item_name = request.form['item_name']
    # Check if item exists
    if not item_exists(item_name):
        return jsonify({'error': 'item does not exist'})
    # Remove item from database
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('DELETE FROM items WHERE name = ?', (item_name,))
    db.commit()
    db.close()
    # Return item info
    return jsonify({'item_name': item_name})

### END ADMIN FUNCTIONS ###


### Running the server ###
'''
# Delete database file
if os.path.exists(database_path):
    os.remove(database_path)
'''
# Create new database if it doesn't exist
if not os.path.exists(database_path):
    initialize_db()
    ## Add admin details to database
    # Create database connection
    db = connect_db()
    db_cur = db.cursor()
    # Get admin username and password from config file
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        # Get admin details (username, password, email)
        admin_username = config['admin']['username']
        admin_password = config['admin']['password']
        admin_email = config['admin']['email']
        # Get salt and hash from password
        salt = os.urandom(16)
        hash = get_hash(admin_password, salt)
        # Insert admin into user table using cursor
        db_cur.execute('INSERT INTO users (username, hash, salt, email, permissions) VALUES (?, ?, ?, ?, ?)', (admin_username, hash, salt, admin_email, 'admin'))
    # Commit changes to database
    db.commit()
    db.close()

# Run flask server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969, debug=True)
