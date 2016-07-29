'''
Created on Jul 7, 2016

@author: rbhat
'''
from datetime import datetime
from kafka import KafkaConsumer
import random
import six
import sys


class Consumer(object):

    def __init__(self, topic, addr):
        self.topic = topic
        self.consumer = KafkaConsumer(bootstrap_servers=addr, auto_offset_reset='earliest')

    def consume_msgs(self):
        self.consumer.subscribe([self.topic])
        
        for message in self.consumer:
            print (message)


if __name__ == "__main__":
    #args = sys.argv
    topic = "test"
    ip_addr = "deepc04.acis.ufl.edu:9092" #str(args[1])
    cons = Consumer(topic, ip_addr)
    cons.consume_msgs()


