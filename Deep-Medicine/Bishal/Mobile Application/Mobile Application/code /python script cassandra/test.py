#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time
from array import array

def testing():
    def testmethod(self):
     print "starting to print"

     try:
        with open('/Users/bishalgautam/Desktop/PrismaP Lab/csv data/ICD9_pr1.csv','rb') as fp:
            for line in fp:
               # print line
                strvalue = array(line.split(';'))
                print (strvalue[0])
     except:
         print "Failed to open the file"

def main():
    testob = testing()
    testob.testmethod()
    print "stop it"

if __name__ == "__main__":
    main()