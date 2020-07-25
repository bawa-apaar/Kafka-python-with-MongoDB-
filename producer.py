from kafka import KafkaProducer
from json import dumps 

#Create Kafka Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

message = {"action":"I", "cargo_number": "W19JE5" ,"driver_id":  "{'license' : 'HR0520111596589', 'date_of_issue': '21-06-2011', 'validity': '21-08-2031'}", 
           "date_of_birth": "18-05-1994", "country_code":"IN", "state_code":"HR", "modified_datetime": 65896321}

message = str(message).encode("utf-8")

#message = {"action":"U", "cargo_number": "PL34A5" ,"driver_id":  "{'license' : 'PB1020111596589', 'date_of_issue': '21-06-2011', 'validity': '21-08-2031'}", 
#          "date_of_birth": "18-05-1994", "country_code":"IN", "driver_name": "Satya", "state_code":"PB", "driver_qualification": "12th pass" ,"modified_datetime": 85896324}

#message = str(message).encode("utf-8")

#message = {"action":"D", "cargo_number": "PL34A5" ,"driver_id":  "{'license' : 'PB1020111596589', 'date_of_issue': '21-06-2011', 'validity': '21-08-2031'}", 
#            "driver_qualification": "12th pass" ,"modified_datetime": 85896324}

#message = str(message).encode("utf-8")

#Send the message from topic ('test_topic')
producer.send('test_topic', value=message)