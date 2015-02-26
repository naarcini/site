#!/usr/bin/python

import http.client
import urllib.parse
import time

# Make sure database is completely reset before starting

NUM_TESTS = 5
BASE_URL = 'localhost:8000'
ROBOT_URL = '/robot/'
UI_URL = '/userInterface/'
MAP_URL = '/visualMap/'
RESET_URL = '/masterReset/'

def PrintAvg(message, timeArray):
    """
    Print the average of the array in ms
    """
    if not isinstance(timeArray, list):
        raise Exception("really?")

    result = 0
    for i in timeArray:
        result += i

    result = (result / len(timeArray)) * 1000
    print('{message}: {time}'.format(message=message, time=result))

# Generate Map
start = time.time()
conn = http.client.HTTPConnection(BASE_URL, timeout=2000)
conn.request('DELETE',RESET_URL)
response = conn.getresponse()
end = time.time()
print('Map generation yielded status {status} and time: {time} ms'.format(status = response.status, time = (end - start) * 1000))

# Reset Map
results = []
for i in range(0, NUM_TESTS):
    start = time.time()
    conn = http.client.HTTPConnection(BASE_URL)
    conn.request('DELETE',RESET_URL)
    response = conn.getresponse()
    end = time.time()
    print(response.status)
    results.append(end - start)
PrintAvg('Map Reset', results)

# Load map (Note: Need to fiddle with views first)
results = []
for i in range(0, NUM_TESTS):
    start = time.time()
    conn = http.client.HTTPConnection(BASE_URL)
    conn.request('GET',MAP_URL)
    response = conn.getresponse()
    end = time.time()
    print(response.status)
    results.append(end - start)
PrintAvg('Map Load', results)

# Write Robot Data (Make sure serverFunctions just writes hardcoded crap)
results = []
for i in range(0, NUM_TESTS):
    start = time.time()
    conn = http.client.HTTPConnection(BASE_URL)
    conn.request('POST',ROBOT_URL)
    response = conn.getresponse()
    end = time.time()
    print(response.status)
    results.append(end - start)
PrintAvg('Write Robot Data', results)

# Read Robot Data (Again, no checking)
results = []
for i in range(0, NUM_TESTS):
    start = time.time()
    conn = http.client.HTTPConnection(BASE_URL)
    conn.request('GET',ROBOT_URL)
    response = conn.getresponse()
    end = time.time()
    print(response.status)
    results.append(end - start)
PrintAvg('Read Robot Data', results)

