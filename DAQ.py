# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 13:51:48 2015

@author: Andrew Erskine
"""

# region [Import]
from PyDAQmx import *
from ctypes import *
import Utils as Util
import numpy
import matplotlib.pyplot as plt

# region [DigitalTasks]


class DigitalInput(Task):
    def __init__(self, device, channels, samprate, secs):
        Task.__init__(self)
        self.CreateDIChan(device, "", DAQmx_Val_ChanPerLine)

        self.read = int32()
        self.totalLength = numpy.uint32(samprate * secs)
        self.digitalData = numpy.zeros((channels, self.totalLength), dtype=numpy.uint32)

        self.CfgSampClkTiming('', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.AutoRegisterDoneEvent(0)

        self.StartTask()
        self.ReadDigitalU32(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.digitalData,
                            self.totalLength * channels, byref(self.read), None)

    def DoneCallback(self, status):
        print status
        self.StopTask()
        self.ClearTask()
        return 0


class TriggeredDigitalInput(Task):
    def __init__(self, device, channels, samprate, secs, trigger_source):
        Task.__init__(self)
        self.CreateDIChan(device, "", DAQmx_Val_ChanPerLine)

        self.read = int32()
        self.totalLength = numpy.uint32(samprate * secs)
        self.digitalData = numpy.zeros((channels, self.totalLength), dtype=numpy.uint32)

        self.CfgSampClkTiming('', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.CfgDigEdgeStartTrig(trigger_source, DAQmx_Val_Rising)
        self.AutoRegisterDoneEvent(0)

        self.StartTask()
        self.ReadDigitalU32(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.digitalData,
                            self.totalLength * channels, byref(self.read), None)

    def DoneCallback(self, status):
        print status.value
        self.StopTask()
        self.ClearTask()
        return 0


class DigitalOut(Task):
    def __init__(self, device, samprate, secs, write):
        Task.__init__(self)
        self.CreateDOChan(device, "", DAQmx_Val_ChanPerLine)

        self.sampsPerChanWritten = int32()
        self.totalLength = samprate * secs
        self.CfgSampClkTiming('', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))

        self.AutoRegisterDoneEvent(0)

        write = Util.binaryToDigitalMap(write)
        self.WriteDigitalU32(write.shape[1], 0, -1, DAQmx_Val_GroupByChannel, write, byref(self.sampsPerChanWritten),
                             None)

        self.StartTask()

    def DoneCallback(self, status):
        print status.value
        self.StopTask()
        self.ClearTask()
        return 0


# region [AnalogTasks]


class AnalogInput(Task):
    def __init__(self, device, channels, samprate, secs):
        Task.__init__(self)
        self.CreateAIVoltageChan(device, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.read = int32()
        self.totalLength = numpy.uint32(samprate*secs)
        self.analogRead = numpy.zeros((channels, self.totalLength), dtype=numpy.float64)

        self.CfgSampClkTiming('', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.AutoRegisterDoneEvent(0)

        self.StartTask()
        self.ReadAnalogF64(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogRead, self.totalLength*channels,
                           byref(self.read), None)

    def DoneCallback(self, status):
        print status
        self.StopTask()
        self.ClearTask()
        return 0


class TriggeredAnalogInput(Task):
    def __init__(self, device, channels, samprate, secs, trigger_source):
        Task.__init__(self)
        self.CreateAIVoltageChan(device, "", DAQmx_Val_Cfg_Default, -10.0, 10.0, DAQmx_Val_Volts, None)

        self.read = int32()
        self.totalLength = numpy.uint32(samprate*secs)
        self.analogRead = numpy.zeros((channels, self.totalLength), dtype=numpy.float64)

        self.CfgSampClkTiming('', samprate, DAQmx_Val_Rising, DAQmx_Val_FiniteSamps, numpy.uint64(self.totalLength))
        self.WaitUntilTaskDone(-1)
        self.CfgDigEdgeStartTrig(trigger_source, DAQmx_Val_Rising)
        self.AutoRegisterDoneEvent(0)

        self.StartTask()
        self.ReadAnalogF64(self.totalLength, -1, DAQmx_Val_GroupByChannel, self.analogRead, self.totalLength*channels,
                           byref(self.read), None)

    def DoneCallback(self, status):
        print status
        self.StopTask()
        self.ClearTask()
        return 0

# TODO TESTING #
# DigitalOut('cDAQ1Mod1/port0/line0, cDAQ1Mod2/port0/line0',1000.0,1.0,numpy.zeros((2,1000)))

# out = DigitalInput('cDAQ1Mod2/port0/line0:1', 2, 1000.0, 1.0)

# out = TriggeredDigitalInput('cDAQ1Mod2/port0/line0:1', 2, 1000.0, 1.0, '/cDAQ1/PFI0')
# plt.plot(out.digitalData[0])

# out = TriggeredAnalogInput('cDAQ1Mod3/ai0:1', 2, 1000.0, 1.0, '/cDAQ1/PFI0')
# plt.plot(out.analogRead[0])