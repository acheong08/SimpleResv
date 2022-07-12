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

# Create two tables: users, reservations, and devices
def initialize_db():
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        email TEXT NOT NULL,
        permissions TEXT NOT NULL
    )''')
    db_cur.execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        device TEXT NOT NULL,
        status TEXT NOT NULL
    )''')
    db_cur.execute('''CREATE TABLE IF NOT EXISTS devices (
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

# Get readable time from a timestamp
def get_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Convert timestamp to readable time
def get_readable_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Convert readable time to timestamp
def get_timestamp(readable_time):
    return timestamp.get_timestamp(readable_time)

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

def device_exists(device_name):
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Check if device exists
    device = db_cur.execute('SELECT * FROM devices WHERE name = ?', (device_name,)).fetchone()
    # Close db connection
    db.close()
    # Return True if device exists
    return device is not None

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
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Get username and password from request
    username = request.form['username']
    password = request.form['password']
    # Check if username exists
    user = db_cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'})
    # Authenticate user
    if not authenticate(username, password):
        return jsonify({'error': 'Invalid password'})
    # Close database connection
    db.close()
    # Return user info
    return jsonify({'username': user[1], 'permissions': user[5]})

# Get list of devices
@app.route('/devices', methods=['GET'])
def get_devices():
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Get list of devices from database
    devices = db_cur.execute('SELECT * FROM devices').fetchall()
    # Close database connection
    db.close()
    # Return list of devices
    return jsonify(devices)

# Get list of reservations
@app.route('/reservations', methods=['GET'])
def get_reservations():
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Get list of reservations from database
    reservations = db_cur.execute('SELECT * FROM reservations').fetchall()
    # Close database connection
    db.close()
    # Return list of reservations
    return jsonify(reservations)

# Handle reservation request
@app.route('/reserve', methods=['POST'])
def reserve():
    # Define db and db_cur
    db = connect_db()
    db_cur = db.cursor()
    # Get username, password, start time, end time, and device from request
    username = request.form['username']
    password = request.form['password']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    device = request.form['device']
    # Authenticate user
    if not authenticate(username, password):
        # Close database connection
        db.close()
        return jsonify({'error': 'Authentication failed'})
    # Check if device exists
    device = db_cur.execute('SELECT * FROM devices WHERE name = ?', (device,)).fetchone()
    if device is None:
        # Close database connection
        db.close()
        return jsonify({'error': 'Device not found'})
    # Check if device is available
    reservation = db_cur.execute('SELECT * FROM reservations WHERE device = ?', (device[1])).fetchone()
    if reservation is not None:
        # Close database connection
        db.close()
        return jsonify({'error': 'Device is not available'})
    # Check if start time is before end time
    if readable_to_timestamp(start_time) > readable_to_timestamp(end_time):
        # Close database connection
        db.close()
        return jsonify({'error': 'Start time is after end time'})
    # Check if start time is after current time
    if readable_to_timestamp(start_time) < timestamp.now():
        # Close database connection
        db.close()
        return jsonify({'error': 'Start time is before current time'})
    # Check if end time is after current time
    if readable_to_timestamp(end_time) < timestamp.now():
        # Close database connection
        db.close()
        return jsonify({'error': 'End time is before current time'})
    # Check if start time is before end time of previous reservation
    reservation = db_cur.execute('SELECT * FROM reservations WHERE start_time < ? AND end_time > ?', (readable_to_timestamp(end_time), readable_to_timestamp(start_time))).fetchone()
    if reservation is not None:
        if readable_to_timestamp(start_time) < readable_to_timestamp(reservation[2]):
            # Close database connection
            db.close()
            return jsonify({'error': 'Start time is before end time of previous reservation'})
    # Check if end time is after start time of next reservation
    reservation = db_cur.execute('SELECT * FROM reservations WHERE start_time > ? AND end_time < ?', (readable_to_timestamp(start_time), readable_to_timestamp(end_time))).fetchone()
    if reservation is not None:
        if readable_to_timestamp(end_time) > readable_to_timestamp(reservation[1]):
            # Close database connection
            db.close()
            return jsonify({'error': 'End time is after start time of next reservation'})
    # Insert reservation into database
    db_cur.execute('INSERT INTO reservations (username, device, start_time, end_time) VALUES (?, ?, ?, ?)', (username, device[1], readable_to_timestamp(start_time), readable_to_timestamp(end_time)))
    # Commit changes
    db.commit()
    # Close database connection
    db.close()
    # Return reservation info
    return jsonify({'username': username, 'device': device[1], 'start_time': start_time, 'end_time': end_time, 'status': 'pending'})

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
    return jsonify({'username': username, 'device': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'cancelled'})

### END USER FUNCTIONS ###


### Admin functions ###

# Authenticate and check if user is admin
def authenticate_admin(username, password):
    # Check if username exists
    if not username_exists(username):
        return False
    if user is None:
        return False
    # Get hash and salt from database
    db = connect_db()
    db_cur = db.cursor()
    user = db_cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    db.close()
    # Check if password is valid
    if hash_salt[0] != get_hash(password, hash_salt[1]):
        return False
    # Check if user is admin
    if user[3] != 'admin':
        return False
    # Return True if user is admin
    return True

# lend reservation (Only admin can lend)
@app.route('/admin/lend', methods=['POST'])
def lend():
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
    return jsonify({'username': username, 'device': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'lent'})

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
    return jsonify({'username': username, 'device': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'returned'})

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
    # Generate new salt and hash password
    new_salt = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    new_hash = get_hash(new_password, new_salt)
    # Check if user already exists
    if user_exists(new_username):
        return jsonify({'error': 'User already exists'})
    # Insert new user into database
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)', (new_username, new_hash, new_salt, new_email, new_permissions, 'active'))
    db.commit()
    db.close()
    # Return new user info
    return jsonify({'username': new_username, 'permissions': new_permissions})

# Add new device (Only admin can add new device)
@app.route('/admin/add_device', methods=['POST'])
def add_device():
    # Authenticate admin
    if not authenticate_admin(request.form['username'], request.form['password']):
        return jsonify({'error': 'Authentication failed'})
    # Get new device name and description from request
    new_device_name = request.form['new_device_name']
    new_device_description = request.form['new_device_description']
    # Check if device name already used
    if device_exists(new_device_name):
        return jsonify({'error': 'Device already exists'})
    # Insert new device into database with status 'available'
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('INSERT INTO devices VALUES (?, ?, ?)', (new_device_name, new_device_description, 'available'))
    db.commit()
    db.close()
    # Return new device info
    return jsonify({'device_name': new_device_name, 'device_description': new_device_description, 'status': 'available'})

# Remove device (Only admin can remove device)
@app.route('/admin/remove_device', methods=['POST'])
def remove_device():
    # Authenticate admin
    if not authenticate_admin(request.form['username'], request.form['password']):
        return jsonify({'error': 'Authentication failed'})
    # Get device name from request
    device_name = request.form['device_name']
    # Check if device exists
    if not device_exists(device_name):
        return jsonify({'error': 'Device does not exist'})
    # Remove device from database
    db = connect_db()
    db_cur = db.cursor()
    db_cur.execute('DELETE FROM devices WHERE device_name = ?', (device_name,))
    db.commit()
    db.close()
    # Return device info
    return jsonify({'device_name': device_name})

### END ADMIN FUNCTIONS ###


### Running the server ###

# Delete database file
if os.path.exists(database_path):
    os.remove(database_path)

# Create new database if it doesn't exist
initialize_db()

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
    app.run(host='127.0.0.1', port=6969, debug=True)