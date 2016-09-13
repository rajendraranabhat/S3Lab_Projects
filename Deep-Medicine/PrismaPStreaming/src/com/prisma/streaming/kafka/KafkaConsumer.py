'''
Created on Sep 6, 2016

@author: rbhat
'''
from kafka import KafkaConsumer


def Consumer():
    #consumer = KafkaConsumer(b"test", group_id=b"my_group", metadata_broker_list=["deepc04.acis.ufl.edu:9092"])
    consumer = KafkaConsumer(bootstrap_servers='deepc04.acis.ufl.edu:9092', auto_offset_reset='earliest')
    consumer.subscribe(['test'])
        
    for message in consumer:
        # This will wait and print messages as they become available
        print(message)


#Consumer()
