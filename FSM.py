from enum import Enum
from Event import Event
#The startStateFetcher should be a callable returning initial state
#This is done to suppport the state machines which have multiple entry points, so that
#the callable can point to the appropriate starting point depending on the conditions
#in which the state machine was started
class FSMException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class FinalityReachedException(FSMException):
    def __init__(self):
        super().__init__("State machine can't accept events anymore as it has already reached finality")

class EventErrors(Enum):
    unhandledEvent = 'unhandled'
    conditionalReject = 'conditionalReject'

class SpecialEvents(Enum):
    defer = 'defer'

class FSM:
    def __init__(self, startStateFetcher):
        self.currState = LauncherState(startStateFetcher())
        self.prevState = None
        self.endingNotifier = Event()
        self.deferalQueue = []
        self.conclusion = None

    def start(self):
        self.handleEvent("launch")

    def findNextState(self, evt, *args):
        nextState = self.currState.react(evt, *args)
        if EventErrors.unhandledEvent == nextState:
            childStateMachine = self.currState if issubclass(type(self.currState), FSM) else None
            while EventErrors.unhandledEvent == nextState and childStateMachine is not None:
                try:
                    nextState = childStateMachine.handleEvent(evt, *args)
                except FinalityReachedException:
                    #This Exception means that the state is atomic, so we set childStateMachine = None 
                    childStateMachine = None
            return EventErrors.unhandledEvent
        else:
            return nextState

    def handleStateEntry(self, state):
        res = state.after_entry()
        childStateMachine = (state  
                             if issubclass(type(state), FSM) else
                             None)
        if childStateMachine is None:
            return res
        else:
            return childStateMachine.start()

    def handleStateExit(self, state):
        childStateMachine = (state  
                            if issubclass(type(state), FSM) else
                            None)
        if childStateMachine is not None:
            self.handleStateExit(childStateMachine.currState)
        state.before_exit()

    def handleEvent(self, evt, *args):
        if(self.currState.isFinal):
            raise FinalityReachedException()
        nextState = self.findNextState(evt, *args)
        if EventErrors.unhandledEvent == nextState:
            self.onUnconsumedEvt(evt)
        elif EventErrors.conditionalReject == nextState:
            self.onConditionalReject(evt)
        elif SpecialEvents.defer == nextState:
            self.deferalQueue.append([evt, args])
        elif nextState != None:
            self.handleStateExit(self.currState)
            self.prevState = self.currState
            self.currState = nextState
            endResult = self.handleStateEntry(self.currState)
            if self.currState.isFinal:
                self.conclusion = endResult
                self.endingNotifier(self.conclusion)
            else:
                self.processDeferalQueueLoop()

    def processDeferalQueueLoop(self):
        localQueue = []
        localQueue, self.deferalQueue = self.deferalQueue, localQueue
        while 0 < len(localQueue):
            nextEvt = localQueue[0]
            self.handleEvent(nextEvt[0], *nextEvt[1])
            localQueue.pop(0)

    def registerForEnd(self, callback):
        self.endingNotifier += callback

    def onUnconsumedEvt(self, evt):
        pass

    def onConditionalReject(self, evt):
        pass


class FSMState:
    def __init__(self, isFinal):
        self.isFinal = isFinal

    def after_entry(self):
        pass

    def before_exit(self):
        pass

    def react(self, evt, *args):
        funcName = "on_" + evt
        if hasattr(self, funcName):
            return getattr(self, funcName)(*args)
        else:
            return EventErrors.unhandledEvent

class CompositeState(FSMState, FSM):
    def __init__(self, startStateFetcher):
        FSMState.__init__(self, False)
        FSM.__init__(self, startStateFetcher)

class LauncherState(FSMState):
    def __init__(self, initialState):
        super().__init__(False)
        self.initialState = initialState

    def on_launch(self):
        return self.initialState