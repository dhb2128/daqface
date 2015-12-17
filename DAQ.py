# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 13:51:48 2015

@author: Andrew Erskine
"""

# region [Import]
from PyDAQmx import *
from ctypes import *
import Utils as util
import numpy 
import time

#TODO just for testing!
import matplotlib.pyplot as plt

#class DigitalInput():
#    def __init__(self,handle,device,channels):
##        Initialise task
#        self.handle = TaskHandle(handle)
#        self.device = device
#        self.channels = channels
#        
#    def createTasks(self):
##        Tell NIDAQ that task should be digital input
#        DAQmxCreateTask("",byref(self.handle))
#        
#        DAQmxCreateDIChan(self.handle,self.device,"",DAQmx_Val_ChanPerLine)
#        
#    def read(self,sampRate,secs):
##        Total number of samples to read
#        totalLength = numpy.uint32(sampRate*secs)      
#        
##        Output - total number of samples actually read
#        read = int32()
#        
##        Array into which to read the data
#        digitalData = numpy.zeros((self.channels,totalLength), dtype=numpy.uint32)
#        
##        Set the acquisition rate for the samples and ensure that task only cleared when finished
#        DAQmxCfgSampClkTiming(self.handle,'',sampRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,numpy.uint64(totalLength))
#        DAQmxWaitUntilTaskDone(self.handle,-1)
#
##        Read the digital data
#        DAQmxReadDigitalU32(self.handle,totalLength,-1,DAQmx_Val_GroupByChannel,digitalData,totalLength*self.channels,byref(read),None)
#
##        Clear the tasks
#        clearTasks(self.handle,None,None)
#        
##        Return the data
#        return digitalData
        
#    def inputTriggeredRead(self,sampRate,secs,triggerSource):
##        Starts the digital input task on a specified trigger source        
#        
##        Total number of samples to read
#        totalLength = numpy.uint32(sampRate*secs)      
#        
##        Output - total number of samples actually read
#        read = int32()
#        
##        Array into which to read the data
#        digitalData = numpy.zeros((self.channels,totalLength), dtype=numpy.uint32)
#        
##        Set the acquisition rate for the samples and ensure that task only cleared when finished
#        DAQmxCfgSampClkTiming(self.handle,'',sampRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,numpy.uint64(totalLength))
#        DAQmxWaitUntilTaskDone(self.handle,-1)
#        
##        Set the trigger source to begin acquisition
#        DAQmxCfgDigEdgeStartTrig(self.handle,triggerSource,DAQmx_Val_Rising)
#
##        Read the digital data
#        DAQmxReadDigitalU32(self.handle,totalLength,-1,DAQmx_Val_GroupByChannel,digitalData,totalLength*self.channels,byref(read),None)
#
##        Clear the tasks
#        clearTasks(self.handle,None,None)
#        
##        Return the data
#        return digitalData
#        
#    def clearTasks(self):
#        DAQmxStopTask(self.handle)
#        DAQmxClearTask(self.handle)
  
class DigitalInput(Task):
    def __init__(self,device,channels,sampRate,secs):
        Task.__init__(self)
        self.CreateDIChan(device,"",DAQmx_Val_ChanPerLine)
        
        self.read = int32()
        self.totalLength = numpy.uint32(sampRate*secs)
        self.digitalData = numpy.zeros((channels,self.totalLength), dtype=numpy.uint32)
        
        self.CfgSampClkTiming('',sampRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.AutoRegisterDoneEvent(0)
        
        self.StartTask()
        self.ReadDigitalU32(self.totalLength,-1,DAQmx_Val_GroupByChannel,self.digitalData,self.totalLength*channels,byref(self.read),None)
        
    def DoneCallback(self,status):
        self.StopTask()
        self.ClearTask()
        return 0
        
class TriggeredDigitalInput(Task):
    def __init__(self,device,channels,sampRate,secs,triggerSource):
        Task.__init__(self)
        self.CreateDIChan(device,"",DAQmx_Val_ChanPerLine)
        
        self.read = int32()
        self.totalLength = numpy.uint32(sampRate*secs)
        self.digitalData = numpy.zeros((channels,self.totalLength), dtype=numpy.uint32)
        
        self.CfgSampClkTiming('',sampRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.CfgDigEdgeStartTrig(triggerSource,DAQmx_Val_Rising)
        self.AutoRegisterDoneEvent(0)
        
        self.StartTask()
        self.ReadDigitalU32(self.totalLength,-1,DAQmx_Val_GroupByChannel,self.digitalData,self.totalLength*channels,byref(self.read),None)
    def DoneCallback(self,status):
        self.StopTask()
        self.ClearTask()
        return 0
  
class DigitalOut(Task):
    def __init__(self,device,sampRate,secs,write):
        Task.__init__(self)
        self.CreateDOChan(device,"",DAQmx_Val_ChanPerLine)
        
        self.sampsPerChanWritten = int32()
        self.totalLength = sampRate*secs
        self.CfgSampClkTiming('',sampRate,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,numpy.uint64(self.totalLength))
        
        self.AutoRegisterDoneEvent(0)
        
        write = util.binaryToDigitalMap(write)
        self.WriteDigitalU32(write.shape[1],0,-1,DAQmx_Val_GroupByChannel,write,byref(self.sampsPerChanWritten),None)
        
        self.StartTask()
    def DoneCallback(self,status):
        self.StopTask()
        self.ClearTask()
        return 0
 
def clearTasks(self,handle, status, callbackData):
    DAQmxStopTask(handle)
    DAQmxClearTask(handle)
    return 0
        
#TODO TESTING #
#DigitalOut('cDAQ1Mod1/port0/line0, cDAQ1Mod2/port0/line0',1000.0,1.0,numpy.zeros((2,1000)))  
        
#out = DigitalInput('cDAQ1Mod2/port0/line0:1',2,1000.0,1.0)
#plt.plot(out.digitalData[0])

out = TriggeredDigitalInput('cDAQ1Mod2/port0/line0:1',2,1000.0,1.0,'/cDAQ1/PFI0')
plt.plot(out.digitalData[0])
