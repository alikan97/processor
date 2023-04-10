import datetime
import requests
import json
import os

HOST = os.environ.get('SPLUNK_HOST')
LOG_URI = "/services/collector/event"
RAW_URI = "/services/collector/raw" # Used for raw data indexing, searcing & Visualising
API_KEY = os.environ.get('SPLUNK_API_KEY')
PORT = os.environ.get('SPLUNK_PORT')

class Log_Level():
    SUCCESS = 1
    DEBUG = 2
    WARN = 3
    ERROR = 4

def send_log(level: Log_Level, message):
    event = {
        'timestamp': datetime.datetime.now(),
        'level': level,
        'message': message
    }

    response = requests.post(HOST+LOG_URI,
                             headers={"Authorization": f'Splunk {API_KEY}'},
                             data=json.dumps(event, ensure_ascii=False).encode('utf-8'))
    
    return response

def send_data(data):
    response = requests.post(HOST+RAW_URI,
                             headers={"Authorization": f'Splunk {API_KEY}'},
                             data=json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    return response