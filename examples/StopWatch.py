import asyncio
from datetime import datetime
import time
import os, sys
parentDir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentDir) 
from FSM import FSM, FSMState, FinalityReachedException

#State machines states can be a new concept to some.
#If that's the case with you, it is encouraged to see the pictorial representation of the
#State machine(StopWatch.png) represented by this code to better understand it. 
class StopWatch(FSM):
    def __init__(self):
        super().__init__(lambda : Stopped())

class Stopped(FSMState):
    def __init__(self):
        super().__init__(False)
        
    def after_entry(self):
        print("Stopwatch stopped state at: ", datetime.now())

    def before_exit(self):
        print("Stopwatch leaving Stopped state at: ", datetime.now())
    
    def on_start(self):
        print("Stopwatch recieved start event at: ", datetime.now())
        return Running()
    
    def on_switchoff(self):
        print("Stopwatch recieved switchoff event at: ", datetime.now())
        return SwitchedOff()

class Running(FSMState):
    def __init__(self):
        super().__init__(False)
        self.lap = 0
        self.initTime = None
        
    def after_entry(self):
        self.initTime = datetime.now()
        print("Running state at: ", self.initTime)

    def before_exit(self):
        print("Stopwatch leaving Running state at: ", datetime.now())
    
    def on_stop(self):
        print("Stopwatch recieved stop event at: ", datetime.now())
        return Stopped()

    def on_switchoff(self):
        print("Stopwatch recieved switchoff event at: ", datetime.now())
        return SwitchedOff()

    def on_lap(self):
        self.lap += 1
        print("Stopwatch lap ", self.lap, " time : ", int((datetime.now() - self.initTime).total_seconds()), " sec")



class SwitchedOff(FSMState):
    def __init__(self):
        super().__init__(True)
        
    def after_entry(self):
        print("Stopwatch switched off at: ", datetime.now())


def stopWatchSimpleDemo():
    stopWatch = StopWatch()
    stopWatch.start()
    
    try:
        time.sleep(2)
        stopWatch.handleEvent("start")
        time.sleep(2)
        stopWatch.handleEvent("lap")
        time.sleep(2)
        stopWatch.handleEvent("lap")
        time.sleep(2)
        stopWatch.handleEvent("stop")
        time.sleep(2)
        stopWatch.handleEvent("switchoff")
        stopWatch.handleEvent("switchoff")
    except FinalityReachedException as ex:
        print(str(ex))

stopWatchSimpleDemo()


