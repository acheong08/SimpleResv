# This is meant to be imported and used as a module.
# It is not meant to be run directly.

### Imports for tests ###
import time
import datetime

### Utility functions ###
def readable_to_timestamp(readable_time):
    # Convert readable time to datetime object
    readable_time = datetime.datetime.strptime(readable_time, '%Y-%m-%d %H:%M:%S')
    # Convert datetime object to timestamp
    timestamp = int(readable_time.timestamp())
    # Return timestamp
    return timestamp


# Each test is a function that takes arguments and verifies if the arguments are correct.

### Tests for time ###
# Takes a readable time string and verifies if it is a valid time.
def check_time_valid(readable_time):
    # Check if the time is a string.
    if not isinstance(readable_time, str):
        # Debug print
        print('Time is not a string.')
        return False
    # Check if the time is in the correct format of YYYY-MM-DD HH:MM:SS.
    if not readable_time.count('-') == 2 and not readable_time.count(':') == 2:
        # Debug print
        print('Time is not in the correct format of YYYY-MM-DD HH:MM:SS.')
        return False
    # Try to convert the time to a timestamp from format   
    try:
        timestamp = readable_to_timestamp(readable_time)
    except ValueError:
        return False
    # Check if timestamp is in the correct range.
    if timestamp < 0 or timestamp > 2**32:
        return False
    # If the timestamp is before current time, return false.
    if timestamp < time.time():
        return False
    # If all checks pass, return true.
    return True