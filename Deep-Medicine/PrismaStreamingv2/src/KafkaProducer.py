'''
Created on Jul 7, 2016

@author: rbhat
'''
import random
import sys
import six
from datetime import datetime
#from kafka.client import KafkaClient
#from kafka.producer import KeyedProducer
from kafka import KafkaConsumer, KafkaProducer

class Producer(object):

    def __init__(self, topic, addr):
        #self.client = KafkaClient(addr)
        #self.producer = KeyedProducer(self.client)
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=addr)

    def produce_msgs(self, source_symbol):
        price_field = random.randint(800,1400)
        msg_cnt = 0
        while(msg_cnt<=2):
            time_field = datetime.now().strftime("%Y%m%d %H%M%S")
            price_field += random.randint(-10, 10)/10.0
            volume_field = random.randint(1, 1000)
            str_fmt = "{};{};{};{}"
            message_info = str_fmt.format(source_symbol,
                                          time_field,
                                          price_field,
                                          volume_field)
            print source_symbol
            #self.producer.send_messages('price_data', source_symbol, message_info)
            self.producer.send(self.topic, message_info)
            msg_cnt += 1

if __name__ == "__main__":
    #args = sys.argv
    topic = "test"
    ip_addr = "deepc04.acis.ufl.edu:9092" #str(args[1])
    partition_key = "Hello-Message0" #str(args[2])
    prod = Producer(topic, ip_addr)
    prod.produce_msgs(partition_key)


