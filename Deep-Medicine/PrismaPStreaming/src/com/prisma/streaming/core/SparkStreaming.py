'''
Created on Sep 6, 2016

@author: rbhat
'''
from com.prisma.streaming.util import Utility

"""
Kafka Spark Streaming Consumer    
"""

import sys
import os
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from com.prisma.streaming.util.Utility import *
#import pyspark_cassandra
#from pyspark_cassandra import streaming

if __name__ == "__main__":
    
    #if len(sys.argv) != 3:
    #    print("Usage: kafka_spark_consumer_01.py <zk> <topic>", file=sys.stderr)
    #    exit(-1)
    
    #Settong up the environment to run locally.
    #Utility.setEnvironment()
    
    sc = SparkContext(appName="PrismaPStreaming")
    ssc = StreamingContext(sc, 1)

    #zkQuorum, topic = sys.argv[1:]
    
    zkQuorum = "deepc04.acis.ufl.edu:2181"
    topic    = "test"
    
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "PrismaPStreamingKafka", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
    
    
    