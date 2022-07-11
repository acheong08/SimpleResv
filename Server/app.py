# Flask API for a reservation system
import sqlite3
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, render_template
import random
import hashlib
import timestamp
import datetime


### Configure Flask app ###

# Define default flask configurations
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# Set flask secret key as urandom string
app.config['SECRET_KEY'] = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

# Define other configurations
database_path = './Data/database.db'


### Helpers ###

# Define database connection and cursor
def connect_db():
    return sqlite3.connect(database_path)
def db_cursor():
    return connect_db().cursor()

# Create two tables: users, reservations, and devices
def initialize_db():
    db_cursor().execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        email TEXT NOT NULL,
        permissions TEXT NOT NULL
    ''')
    db_cursor().execute('''CREATE TABLE IF NOT EXISTS reservations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        device TEXT NOT NULL,
        status TEXT NOT NULL
    ''')
    db_cursor().execute('''CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL
    ''')
    connect_db().commit()


### Utility functions ###

# Get hash from a password and salt
def get_hash(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()

# Convert timestamp to human readable format
def timestamp_to_readable(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

# Convert readable timestamp to timestamp
def readable_to_timestamp(readable):
    return timestamp.strptime(readable, '%Y-%m-%d %H:%M:%S')

# Guess the hash type of a hash (SHA-256, SHA-512, etc. and MD5)
def guess_hash_type(hash):
    if len(hash) == 64:
        return 'SHA-256'
    elif len(hash) == 128:
        return 'SHA-512'
    elif len(hash) == 32:
        return 'MD5'
    else:
        return 'Unknown'


### User functions ###

# Authenticate users
def authenticate(username, password):
    # Check if username exists
    db_cursor().execute('SELECT * FROM users WHERE username = ?', (username,))
    user = db_cursor().fetchone()
    if user is None:
        return False
    # Get hash and salt from database
    db_cursor().execute('SELECT hash, salt FROM users WHERE username = ?', (username,))
    hash_salt = db_cursor().fetchone()
    # Check if password is valid
    if hash_salt[0] != get_hash(password, hash_salt[1]):
        return False
    # Return True if user is authenticated
    return True

# Handle login request
@app.route('/login', methods=['POST'])
def login():
    # Get username and password from request
    username = request.form['username']
    password = request.form['password']
    # Check if username exists
    db_cursor().execute('SELECT * FROM users WHERE username = ?', (username,))
    user = db_cursor().fetchone()
    if user is None:
        return jsonify({'error': 'User not found'})
    # Check if password is correct
    if user[2] != password:
        return jsonify({'error': 'Password incorrect'})
    # Return user info
    return jsonify({'username': user[1], 'permissions': user[4]})

# Get list of devices
@app.route('/devices', methods=['GET'])
def get_devices():
    # Get list of devices from database
    db_cursor().execute('SELECT * FROM devices')
    devices = db_cursor().fetchall()
    # Return list of devices
    return jsonify(devices)

# Get list of reservations
@app.route('/reservations', methods=['GET'])
def get_reservations():
    # Get list of reservations from database
    db_cursor().execute('SELECT * FROM reservations')
    reservations = db_cursor().fetchall()
    # Return list of reservations
    return jsonify(reservations)

# Handle reservation request
@app.route('/reserve', methods=['POST'])
def reserve():
    # Get username, password, start time, end time, and device from request
    username = request.form['username']
    password = request.form['password']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    device = request.form['device']
    # Authenticate user
    if not authenticate(username, password):
        return jsonify({'error': 'Authentication failed'})
    # Check if device exists
    db_cursor().execute('SELECT * FROM devices WHERE name = ?', (device,))
    device = db_cursor().fetchone()
    if device is None:
        return jsonify({'error': 'Device not found'})
    # Check if device is available
    db_cursor().execute('SELECT * FROM reservations WHERE device = ? AND status = ?', (device[1], 'pending'))
    reservation = db_cursor().fetchone()
    if reservation is not None:
        return jsonify({'error': 'Device is not available'})
    # Check if start time is before end time
    if readable_to_timestamp(start_time) > readable_to_timestamp(end_time):
        return jsonify({'error': 'Start time is after end time'})
    # Check if start time is after current time
    if readable_to_timestamp(start_time) < timestamp.now():
        return jsonify({'error': 'Start time is before current time'})
    # Check if end time is after current time
    if readable_to_timestamp(end_time) < timestamp.now():
        return jsonify({'error': 'End time is before current time'})
    # Check if start time is before end time of previous reservation
    db_cursor().execute('SELECT * FROM reservations WHERE device = ? AND status = ?', (device[1], 'pending'))
    reservation = db_cursor().fetchone()
    if reservation is not None:
        if readable_to_timestamp(start_time) < readable_to_timestamp(reservation[2]):
            return jsonify({'error': 'Start time is before end time of previous reservation'})
    # Check if end time is after start time of next reservation
    db_cursor().execute('SELECT * FROM reservations WHERE device = ? AND status = ?', (device[1], 'pending'))
    reservation = db_cursor().fetchone()
    if reservation is not None:
        if readable_to_timestamp(end_time) > readable_to_timestamp(reservation[1]):
            return jsonify({'error': 'End time is after start time of next reservation'})
    # Insert reservation into database
    db_cursor().execute('INSERT INTO reservations (username, device, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)', (username, device[1], start_time, end_time, 'pending'))
    connect_db().commit()
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
    db_cursor().execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
    reservation = db_cursor().fetchone()
    if reservation is None:
        return jsonify({'error': 'Reservation not found'})
    # Check if username for reservation is correct
    if reservation[0] != username:
        return jsonify({'error': 'Username is incorrect'})
    # Check if reservation is pending
    if reservation[4] != 'pending':
        return jsonify({'error': 'Reservation is not pending'})
    # Cancel reservation
    db_cursor().execute('UPDATE reservations SET status = ? WHERE id = ?', ('cancelled', reservation_id))
    connect_db().commit()
    # Return reservation info
    return jsonify({'username': username, 'device': reservation[2], 'start_time': reservation[3], 'end_time': reservation[4], 'status': 'cancelled'})


### Admin functions ###

# Authenticate and check if user is admin
def authenticate_admin(username, password):
    # Check if username exists
    db_cursor().execute('SELECT * FROM users WHERE username = ?', (username,))
    user = db_cursor().fetchone()
    if user is None:
        return False
    # Get hash and salt from database
    db_cursor().execute('SELECT hash, salt FROM users WHERE username = ?', (username,))
    hash_salt = db_cursor().fetchone()
    # Check if password is valid
    if hash_salt[0] != get_hash(password, hash_salt[1]):
        return False
    # Check if user is admin
    db_cursor().execute('SELECT * FROM users WHERE username = ? AND admin = ?', (username, True))
    user = db_cursor().fetchone()
    if user is None:
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
    db_cursor().execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
    reservation = db_cursor().fetchone()
    if reservation is None:
        return jsonify({'error': 'Reservation not found'})
    # Check if username for reservation is correct
    if reservation[0] != username:
        return jsonify({'error': 'Username is incorrect'})
    # Check if reservation is pending
    if reservation[4] != 'pending':
        return jsonify({'error': 'Reservation is not pending'})
    # lend reservation
    db_cursor().execute('UPDATE reservations SET status = ? WHERE id = ?', ('lent', reservation_id))
    connect_db().commit()
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
    db_cursor().execute('SELECT * FROM reservations WHERE id = ?', (reservation_id,))
    reservation = db_cursor().fetchone()
    if reservation is None:
        return jsonify({'error': 'Reservation not found'})
    # Check if username for reservation is correct
    if reservation[0] != username:
        return jsonify({'error': 'Username is incorrect'})
    # Check if reservation is lent
    if reservation[4] != 'lent':
        return jsonify({'error': 'Reservation is not lent'})
    # Return reservation
    db_cursor().execute('UPDATE reservations SET status = ? WHERE id = ?', ('returned', reservation_id))
    connect_db().commit()
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
    db_cursor().execute('SELECT * FROM reservations WHERE status = ?', ('lent',))
    reservations = db_cursor().fetchall()
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
    db_cursor().execute('SELECT * FROM reservations WHERE status = ?', ('pending',))
    reservations = db_cursor().fetchall()
    # Check current time
    current_time = datetime.now()
    # Check if reservation is pending
    pending_reservations = []
    for reservation in reservations:
        if reservation[3] > current_time:
            pending_reservations.append(reservation)
    # Return pending reservations
    return jsonify({'pending_reservations': pending_reservations})

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
    # Insert new user into database
    db_cursor().execute('INSERT INTO users (username, hash, salt, email, permissions) VALUES (?, ?, ?, ?, ?)', (new_username, new_hash, new_salt, new_email, new_permissions))
    connect_db().commit()
    # Return new user info
    return jsonify({'username': new_username, 'permissions': new_permissions})