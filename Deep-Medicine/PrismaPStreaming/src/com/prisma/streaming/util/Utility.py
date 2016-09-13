'''
Created on Sep 6, 2016

@author: rbhat
'''
#utility
import ConfigParser
from com.prisma.streaming.util import PrismaProperties
import os
import sys

def setEnvironment():
    # Set the path for spark installation
    # this is the path where you have built spark using sbt/sbt assembly
    os.environ['SPARK_HOME'] = "/home/rbhat/spark-1.6.1-bin-hadoop2.6"
    # Append to PYTHONPATH so that pyspark could be found
    sys.path.append("/home/rbhat/spark-1.6.1-bin-hadoop2.6/python")
    sys.path.append("/home/rbhat/spark-1.6.1-bin-hadoop2.6/python/lib")
    # Now we are ready to import Spark Modules
    
    
def getConfig():
    config = ConfigParser.RawConfigParser()
    config.read("../../../../../resources/config.properties")
    
#Pretty Print
def prettyPrint(msg):
    print msg
    
def readProperties():    
    config = ConfigParser.RawConfigParser()
    #config.read("/home/rbhat/eclipse-scala/workspace/PrismaPStreaming/resources/config.properties")
    config.read("../../../../../resources/config.properties")
    print config.get("Kafka", "topic")
    print type(config.get("Kafka", "topic"))
    
#readProperties()
 
#print type(PrismaProperties.topic), PrismaProperties.topic


#cwd = os.getcwd()
#print cwd



import os
import sys

#print os.environ['SPARK_HOME']
#print os.environ














