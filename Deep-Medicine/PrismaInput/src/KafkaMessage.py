'''
Created on Jun 21, 2016

@author: rbhat
'''
import threading, logging, time

from kafka import KafkaConsumer, KafkaProducer
import schedule
import time
import datetime
import main2 as ma

class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')
        #producer = KafkaProducer(bootstrap_servers='deepc04.acis.ufl.edu:9092')
        
        """
        while True:
            producer.send('test', b"testingt123456")
            #producer.send('test', b"TestingAgain!")
        """
        json_message = ma.preprocess()
        producer.send('test', json_message)
        #producer.send('test', b"testingt123456789")
        time.sleep(1)


class Consumer(threading.Thread):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
        consumer.subscribe(['test'])

        for message in consumer:
            print (message)


def main():
    threads = [
        Producer(),
        #Consumer()
    ]

    for t in threads:
        t.start()

    time.sleep(10)
    


"""
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()
    """
    
def job(t):
    main()
    print "I'm working...", t, datetime.datetime.now()
    return
    
schedule.every(1).minutes.do(job,"time: ")
#schedule.every().second().do(job,'It is 01:00')
#schedule.every().day.at("01:00").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute

