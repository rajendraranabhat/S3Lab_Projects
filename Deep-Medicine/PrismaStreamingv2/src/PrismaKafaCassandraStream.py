'''
Created on Jul 7, 2016

@author: rbhat
'''
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pyspark_cassandra
from pyspark_cassandra import streaming
from datetime import datetime
import sys

# Create a StreamingContext with batch interval of 3 second
sc = SparkContext("local[*]", "PrismaStream")
ssc = StreamingContext(sc, 3)

kafkaStream = KafkaUtils.createStream(ssc, "deepc04.acis.ufl.edu:2181", "GroupNameDoesntMatter", {"test": 2})

raw = kafkaStream.flatMap(lambda kafkaS: kafkaS)
time_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
clean = raw.map(lambda xs: xs[1].split(" "))

clean.pprint()

# Test timestamp 1 and timestamp 2
# times = clean.map(lambda x: [x[1], time_now])
# times.pprint()

# test subtract new time from old time
# x = clean.map(lambda x:
#             (datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f') -
#             datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')).seconds)
# x.pprint()


# Match table fields with dictionary keys
# this reads input of format
# partition, timestamp, location, price
my_row = clean.map(lambda x: {
      "testid": "test",
      "time1": "8", #x[1],
      "time2": time_now,
      "location": "3",#x[1],
      "delta": (datetime.strptime(x[1], '%Y-%m-%d %H:%M:%S.%f') -
       datetime.strptime(time_now, '%Y-%m-%d %H:%M:%S.%f')).microseconds,
      "brand": "brand",
      "price": round(float(7), 2) }) #round(float(x[1]), 2) })

my_row.pprint()

my_row.saveToCassandra("testing", "teststream")

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
