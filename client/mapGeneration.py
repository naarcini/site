#!/usr/bin/python

import http.client
import urllib.parse
import time
import threading

NUM_TESTS = 5
BASE_URL = 'nicolasarciniega.com'
MAP_URL = '/visualMap/'

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

def BuildMap():
    """
    Build the map
    """
    results = []
    for i in range(0, NUM_TESTS):
        start = time.time()
        conn = http.client.HTTPConnection(BASE_URL)
        conn.request('GET',MAP_URL + '?robotId=1')
        response = conn.getresponse()
        end = time.time()
        print(response.status)
        results.append(end - start)
    PrintAvg('Build Map', results)

# Single threaded map build
BuildMap()

# 2 threaded Build Map
start = time.time()
threads = []
for i in range(0, 2):
    threads.append(threading.Thread(target=BuildMap))
for i in range(0, 2):
    threads[i].start()
for i in range(0, 2):
    threads[i].join()
print('2-threaded total: {time}'.format(time = (time.time() - start) * 1000))

# 4 threaded Build Map
start = time.time()
threads = []
for i in range(0, 4):
    threads.append(threading.Thread(target=BuildMap))
for i in range(0, 4):
    threads[i].start()
for i in range(0, 4):
    threads[i].join()
print('4-threaded total: {time}'.format(time = (time.time() - start) * 1000))
