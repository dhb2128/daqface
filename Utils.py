# -*- coding: utf-8 -*-
"""
Created on Mon Nov 02 18:16:20 2015

@author: Andrew
"""

import numpy
import math

def binaryToDigitalMap(binBuffer): 
    # If we have a sequence of 1s and 0s corresponding to digital ON and OFF times, we want to map this to digital commands that
    # the digital ports can read and implement. Input should be mapped as a 2d numpy array (dtype=numpy.uint32), rows are individual lines, columns 
    # are continuous time points. Ignores sampling rate until we tell NIDAQmx what it is.   
    
    digital = numpy.zeros((binBuffer.shape[0],binBuffer.shape[1]))   
        
    nLines = digital.shape[0]
    
    for line in range(nLines):
        digital[line] = binBuffer[line] * math.pow(2,(line))
    
    return numpy.uint32(digital)
    
def binaryPulseGenerator(sampRate,channels,offset,tail,odourON,odourOFF,fvON,fvOFF,odourLine,cleaning):
    totalLength = offset+tail+max([(odourOFF),(fvOFF)])+cleaning
        
    binary = numpy.zeros((channels,totalLength), dtype=numpy.uint32) # Note: the 8 is hard coded and corresponds to number of odour lines
    
    binary[odourLine, odourON+offset:odourOFF+offset] = 1
    binary[7, fvON+offset:fvOFF+offset] = 1
    binary[6, fvON+offset:fvOFF+offset] = 1
    binary[6, odourOFF:fvOFF+cleaning] = 1
    
    return binary
    
def closeAllValves():    
    return numpy.zeros((8,10),dtype=numpy.uint32)
    
def trigger(trialLength):
    return numpy.zeros(trialLength,dtype=numpy.uint32)
