import pymongo
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import warnings
warnings.filterwarnings("ignore")
import datetime
from mapping_conversions import convert_keys

consumer = KafkaConsumer('test_topic', bootstrap_servers=['localhost:9092'], enable_auto_commit=False,
                          auto_offset_reset='earliest', group_id='mongodb_test')

mongo_client = MongoClient('localhost:27017')

DRIVER_MAPPING = [('cargo_number', str, 'cargo_number', str),
    ('driver_id', str, 'driver_id', eval),
    ('date_of_birth', str, 'date_of_birth', str),
    ('country_code', str, 'country_code', str),
    ('state_code', str, 'state_code', str), 
    ('driver_name', str, 'driver_name', str),   
    ('driver_qualification', str, 'driver_education', str),   
    ('modified_datetime', int, 'modified_datetime', int)        
]

class Driver:
    def __init__(self, input_message, mongo_client):
        self.input_message = input_message
        self.transform_message()
        self.collection = mongo_client["informatio_database"]["driver"]
        
    def transform_message(self):
        self.transformed_message = convert_keys(self.input_message, DRIVER_MAPPING)
        self.transformed_message['_id'] = 'cargo_number:{}'.format(self.transformed_message["cargo_number"])
        
    def primary_key(self):
        return self.transformed_message['_id'] if '_id' in self.transformed_message else None
     
    def insert(self):
        try:
            insert_stmt = self.collection.insert_one(self.transformed_message)
            print('message <{}> inserted successfully, insert acknowledged <{}>'.format(self.transformed_message, insert_stmt.acknowledged))
            
        except pymongo.errors.DuplicateKeyError as dd:
            print("exception is :-", dd)
    
    def update(self):
        modified_doc = {"$set": self.transformed_message}
        
        upd_stmt = self.collection.update_one({"_id":self.primary_key(),"modified_datetime": {"$lt": self.transformed_message["modified_datetime"]}}, modified_doc)

        print('message <{}> updated successfully, modified acknowledged <{}>'.format(self.transformed_message, upd_stmt.raw_result))
        
    def upsert(self):
        if(self.collection.find({'_id': self.primary_key()}).count() == 0):
            self.insert()
        else:
            self.update()
            
        print('message <{}> upserted successfully'.format(self.transformed_message))
        
    def delete(self):
        del_stmt = self.collection.delete_one({'_id': self.primary_key()})
        print('record with id <{}> deleted successfully, , delete acknowledged <{}>'.format(self.transformed_message, del_stmt.raw_result))
        

def process_messages():
    for message_string in consumer:
        message_string = message_string.value.decode('utf-8')
        try:
            message = eval(message_string)
            
        except NameError as nameError:
            print('Bad message <{}> raised exception <{}> of class <{}>. Marking the message consumed.'.format(message_string,nameError, type(nameError)))
            consumer.commit()
            continue
            
        except Exception as ee:
            print("Bad message <{}> of class <{}>. Marking the message consumed.".format(message_string,nameError, type(ee)))

        a_driver = Driver(message, mongo_client)
        if(message['action'] == "I"):
            a_driver.insert()
        elif(message['action'] == "U"):
            a_driver.upsert()
        elif(message['action'] == "D"):    
            a_driver.delete()
            
        else:
            print('Bad message <{}> has bad action <{}>:'.format(message_string, message['action']))
            
        consumer.commit()
        
if __name__ == '__main__':
    print('Starting process now')
    process_messages()