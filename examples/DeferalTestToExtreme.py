import asyncio
from datetime import datetime
import os, sys
parentDir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentDir) 
from FSM import FSM, FSMState, CompositeState, FinalityReachedException, SpecialEvents

class FSM1(FSM):
    def __init__(self):
        super().__init__(lambda : S1())
    
class S1(FSMState):
    def __init__(self):
        super().__init__(False)

    def on_S2(self):
        return S2()
    
    def on_e1(self, data):
        print("S1:e1, data: ", data)


class S2(FSMState):
    def __init__(self):
        super().__init__(False)

    def on_S1(self):
        return S1()

    def on_S3(self):
        return S3()

    def on_e1(self, data):
        return SpecialEvents.defer
    
    def on_e2(self, data):
        print("S2:e2, data: ", data)

class S3(FSMState):
    def __init__(self):
        super().__init__(False)

    def on_S2(self):
        return S2()
    
    def on_S1(self):
        return SpecialEvents.defer

    def on_e1(self, data):
        return SpecialEvents.defer
    
    def on_e2(self, data):
        return SpecialEvents.defer

#Deferal of deferred events
def demo1():
    print("Deferal of deferred events!")
    fsm = FSM1()
    fsm.start()
    fsm.handleEvent("S2")
    fsm.handleEvent("S3")
    fsm.handleEvent("e1", 1)
    fsm.handleEvent("e1", 2)
    fsm.handleEvent("S2")
    fsm.handleEvent("S1")

#Handling state change whle processing deferral
def demo2():
    print("Changing state while peocessing deferral events!")
    fsm = FSM1()
    fsm.start()
    fsm.handleEvent("S2")
    fsm.handleEvent("S3")
    fsm.handleEvent("e1", 1)
    fsm.handleEvent("e1", 2)
    fsm.handleEvent("S1")
    fsm.handleEvent("e1", 3)
    fsm.handleEvent("e1", 4)
    fsm.handleEvent("S2")

#Some processed, some deferred futher
def demo3():
    print("Some processed, some deferred futher!")
    fsm = FSM1()
    fsm.start()
    fsm.handleEvent("S2")
    fsm.handleEvent("S3")
    #At this point, we are in S3, so the 5 events below will be deferred
    fsm.handleEvent("e1", 1)
    fsm.handleEvent("e2", 1)
    fsm.handleEvent("S1")
    fsm.handleEvent("e1", 2)
    fsm.handleEvent("e2", 2)
    
    #After this line, we will enter S2
    #Some interesting things happen whlile executing line,
    #deferred from the previous state:
    #1. ("e1", 1) will be deffrred further
    #2. ("e2", 1) will be processed
    #3. ("S1") will be processed an the current state state will transition to S1
    #4. ("e1", 1) deferred in the 1st step is now at the front of he deferral queue, so it will be proccssed
    #5. Now since the state is S1 now, ("e1", 2) will be processed as it is handled by S1
    #6. ("e2, 2") will be dropped at it is not supported by S1
    fsm.handleEvent("S2")
    #So after executing this line the final output will be:
    #S2:e2, data:  1
    #S1:e1, data:  1
    #S1:e1, data:  2


demo1()
demo2()
demo3()