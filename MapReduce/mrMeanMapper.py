'''
Created on Feb 21, 2011
Machine Learning in Action Chapter 18
Map Reduce Job for Hadoop Streaming 
mrMeanMapper.py
@author: Peter Harrington
'''
import sys
from numpy import mat, mean, power

def read_input(file):
    for line in file:
        yield line.rstrip()
        
inputs = read_input(sys.stdin)#creates a list of input lines
inputs = [float(line) for line in inputs] #overwrite with floats
numInputs = len(inputs)
inputs = mat(inputs)
sqInput = power(inputs,2)
meanValue=mean(inputs)
meanSqValue=mean(sqInput)
#output size, mean, mean(square values)
print "%d\t%f\t%f" % (numInputs,meanValue , meanSqValue) #calc mean of columns
print >> sys.stderr, "report: still alive" 
