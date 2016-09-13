'''
Created on Sep 6, 2016

@author: rbhat
'''

""" 
    Sends Kafka message producer. Use python version of producer. Please download kafka from http://kafka.apache.org/downloads.html first and follow
    http://kafka.apache.org/documentation.html for setting up the broker/client. Also for python client for kafka please pip https://github.com/mumrah . 
    ie. pip install python-kafka
    
"""

import time
#from kafka import KafkaConsumer, KafkaProducer

from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError


def print_response(response=None):
    if response:
        print('Error: {0}'.format(response[0].error))
        print('Offset: {0}'.format(response[0].offset))


def Producer():
    #producer = KafkaProducer(bootstrap_servers='deepc04.acis.ufl.edu:9092')
    #producer.send('test', b"testingt123456")
    
    kafka = KafkaClient("deepc04.acis.ufl.edu:9092")
    producer = SimpleProducer(kafka)

    topic = b'test'
    msg = b'Hello World from Me/Rajendra!'

    try:
        print_response(producer.send_messages(topic, msg))
    except LeaderNotAvailableError:
        # https://github.com/mumrah/kafka-python/issues/249
        time.sleep(1)
        print_response(producer.send_messages(topic, msg))

    kafka.close()

#Producer()
    
    
