import requests
import time
from datetime import datetime
import json

def elasticsearch_api_injector(data):
    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('pretty', ''),
    )
    tstamp = datetime.fromtimestamp(int(time.time()))
    tstamp = 'T'.join(str(tstamp).split())
    data = { 
            "@timestamp" : tstamp ,
            "epoch_time" : data['epoch_time'] ,
            "memory_usage" : data['memory_usage'] ,
            "active_users" : data['logged_in_users'] ,
            "total_memory" : data['total_memory'] ,
            "swap_usage" : data['swap_usage'] ,
            "ram_usage" : data['ram_usage'] ,
            "processes" : data['processes'] , 
            "min_ping" : data['min_ping'] ,
            "average_ping" : data['average_ping'] ,
            "max_ping" : data['max_ping'] ,
            "user": { 
                "username": data['username'] ,
                "ip_address" : data['ip_address'] ,
            } 
        }
    data = json.dumps(data)
    response = requests.post('http://localhost:9200/ansh-sarkar/_doc/',
                            headers=headers, params=params, data=data)
    print(response.status_code)

