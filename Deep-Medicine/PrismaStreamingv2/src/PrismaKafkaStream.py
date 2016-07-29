'''
Created on Jul 7, 2016

@author: rbhat
'''
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


# Create a local StreamingContext with two working thread and batch interval of 2 second
sc = SparkContext("local[*]", "MyKafkaStream")
ssc = StreamingContext(sc, 1)

kafkaStream = KafkaUtils.createStream(ssc, "deepc04.acis.ufl.edu:2181", "GroupNameDoesntMatter", {"test": 2})

messages = kafkaStream.map(lambda xs:xs)
messages.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate