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
class TestLogin(unittest.TestCase):
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

# Run tests
if __name__ == '__main__':
    unittest.main()
    sys.exit(0)