# Run app.py and test the app
import threading
import time
import subprocess
import os
import sys
import requests
import json
import unittest
import urllib.request
import urllib.parse
import urllib.error


# Define test
class TestAll(unittest.TestCase):
    ### Logging in ###
    # Test /login endpoint with valid admin credentials
    def test_login_valid(self):
        url = 'http://localhost:6969/login'
        data = {'username': 'admin', 'password': 'admin'}
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['username'] == 'admin'
        assert response.json()['permissions'] == 'admin'
    # Test /login endpoint with invalid admin credentials
    def test_login_invalid(self):
        url = 'http://localhost:6969/login'
        data = {'username': 'admin', 'password': 'admin1'}
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['error'] == 'Invalid password'
    
    ### Admin ###
    # Test /admin/add_item endpoint with valid admin credentials
    def test_add_item_valid(self):
        url = 'http://localhost:6969/admin/add_item'
        data = {'username': 'admin', 'password': 'admin', 'new_item_name': 'test_item', 'new_item_description': 'test_desc'}
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['item_name'] == 'test_item'
        assert response.json()['item_description'] == 'test_desc'
        assert response.json()['item_status'] == 'available'
    # Test /admin/remove_item endpoint with valid admin credentials and item_name
    def test_remove_item_valid(self):
        url = 'http://localhost:6969/admin/remove_item'
        data = {'username': 'admin', 'password': 'admin', 'item_name': 'test_item'}
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['item_name'] == 'test_item'
    # Test /admin/register endpoint with valid admin credentials and new_username, new_password, new_email, and new_permissions
    def test_register_valid(self):
        url = 'http://localhost:6969/admin/register'
        data = {
            'username': 'admin', 
            'password': 'admin', 
            'new_username': 'test_user', 
            'new_password': 'test_pass', 
            'new_email': 'user@example.com',
            'new_permissions': 'user'
        }
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['username'] == 'test_user'
        assert response.json()['permissions'] == 'user'
    # Add new item for testing reservation
    def test_add_item_valid2(self):
        url = 'http://localhost:6969/admin/add_item'
        data = {'username': 'admin', 'password': 'admin', 'new_item_name': 'test_item2', 'new_item_description': 'test_desc'}
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['item_name'] == 'test_item2'
        assert response.json()['item_description'] == 'test_desc'
        assert response.json()['item_status'] == 'available'
    # test /reserve with valid username, password, item name, start time, and end time
    def test_reserve_valid(self):
        url = 'http://localhost:6969/reserve'
        data = {
            'username': 'admin', 
            'password': 'admin', 
            'item': 'test_item2', 
            'start_time': '2022-08-01 12:00:00', 
            'end_time': '2022-08-01 13:00:00'
        }
        # Make post request with data
        response = requests.post(url, data=data)
        print(response.json())
        assert response.status_code == 200
        assert response.json()['username'] == 'admin'
        assert response.json()['item'] == 'test_item2'
        assert response.json()['status'] == 'pending'

# Run tests
if __name__ == '__main__':
    unittest.main()
    sys.exit(0)