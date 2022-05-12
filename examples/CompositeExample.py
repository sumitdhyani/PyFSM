import asyncio
from datetime import datetime
import os, sys
parentDir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentDir) 
from FSM import FSM, FSMState, CompositeState, FinalityReachedException


#State machines with composite/nested states can be a new concept to some.
#If that's the case with you, it is encouraged to see the pictorial representation of the
#State machine(Composite_state_machine.png) represented by this code to better understand it. 

class MyFSM(FSM):
    def __init__(self):
        super().__init__(lambda : SC1())

class SC1(CompositeState):
    def __init__(self):
        super().__init__(lambda : SC11())
    
    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
    
    def on_e1(self):
        print("SC1::e1")
        return SC2()

class SC2(CompositeState):
    def __init__(self):
        super().__init__(lambda : SC21())

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")
    
    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
        
    def on_e2(self):
        print("SC2::e2")
        return SC1()
    
    def on_terminate(self):
        print("SC2::terminate")
        return STerminate()

class SC11(FSMState):
    def __init__(self):
        super().__init__(False)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
        
    def on_e11(self):
        print("SC11:e11")
        return SC12()

class SC12(FSMState):
    def __init__(self):
        super().__init__(True)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
        
    def on_e12(self):
        print("SC12:e12")

class SC21(FSMState):
    def __init__(self):
        super().__init__(False)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
        
    def on_e21(sel):
        print("SC21::e21")
        return SC22()

class SC22(FSMState):
    def __init__(self):
        super().__init__(True)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
        
    def on_e22(self):
        print("SC22::e22")

class STerminate(FSMState):
    def __init__(self):
        super().__init__(True)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")


def compositeDemo():
    fsm = MyFSM()
    fsm.start()
    try:
        fsm.handleEvent("e2")
        fsm.handleEvent("e2")
        fsm.handleEvent("e11")
        fsm.handleEvent("e12")
        fsm.handleEvent("e1")
        fsm.handleEvent("e21")
        fsm.handleEvent("terminate")
        #Exception should be thrown here as we have reached finality here
        fsm.handleEvent("e2")
    except FinalityReachedException as ex:
        print(str(ex))

compositeDemo()


