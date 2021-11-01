import asyncio
from datetime import datetime
import os, sys
parentDir = os.path.dirname(os.getcwd())
sys.path.insert(0, parentDir) 
from FSM import FSM, FSMState, CompositeState, FinalityReachedException, SpecialEvents

class Camera(FSM):
    def __init__(self):
        super().__init__(lambda : Shooting())

class Shooting(CompositeState):
    def __init__(self):
        super().__init__(lambda : Idle())

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")

    def on_browse(self):
        print("Shooting::browse")
        return Browsing()

class Browsing(FSMState):
    def __init__(self):
        super().__init__(False)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")

    def on_displayImage(imageName):
        print("Display image, image name: ", imageName)

    def on_shoot(self):
        print("Browsing::shoot")
        return Shooting()

class Idle(FSMState):
    def __init__(self):
        super().__init__(False)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")
    
    def on_focus(self):
        print("Idle::focus")
        return Focusing()

class Focusing(FSMState):
    def __init__(self):
        super().__init__(False)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")

    def on_focused(self):
        print("Focusing::focused")
        return Focused()

    def on_click(self):
        print("Focusing::click")
        return SpecialEvents.defer

class Focused(FSMState):
    def __init__(self):
        super().__init__(False)

    def after_entry(self):
        print(str(type(self).__name__), ".after_entry")

    def before_exit(self):
        print(str(type(self).__name__), ".before_exit")

    def on_click(self):
        print("Focused::click")
        print("Image clicked!")
    
    def on_buttonReleased(self):
        print("Focused::buttonReleased")
        return Idle()

def DeferalDemo():
    fsm = Camera()
    fsm.start()
    try:
        pass
        fsm.handleEvent("focus")
        fsm.handleEvent("click")
        fsm.handleEvent("focused")
    except FinalityReachedException as ex:
        print(str(ex))

DeferalDemo()