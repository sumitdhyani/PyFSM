# AsyncFSM
A python module which provides interface for a finite state machine.

===================================================================================
Basic:
To create a state machine, instantiate a subclass of AFSM class.
This class asks for callable object in its constructor for which should return the initial state.

A state is represented by an object AFSMState's sub-class. It accepts a boolean in constructor which signifies whether the state is final or not.

Any AFSMState subclass must override the on_entry and before_exit methods if it needs to perform some action just after entry and just before exit, respectively for those states in the state machine.

The application can raise an event by invoking the handleEvent method of the state machine, the event will be handled by the current state if thers is method by the name of on_<eventName> in the current state.
To transition to a new state the event handler must return an AFSMState object which will become the new state.

Raising an event on a state machine which has reached final state leads to a "FinalityReachedException" exception.

===================================================================================
Composite states:
The API also supports composite states, these are the states which have one or internal states and run their own state machine within them.
So, conceptually, a CompositeState is both a state and a state machine.
To outside code, only the outermost state is visible and any event passed to a composite state is first attempted to be handled by the outermost state.
If there isn't a handler for the event in the outermost state, then the event is passed to the current inner state and this process goes on untill we find an event handler or we reach the innermost atomic state.

By design the outside code can't directly transition to the inner state of a composite state. They will have to trasnsition to the composite state whose starting state will always be the one returned in the constructor

Also, an inner state can't transition outside its parent state as the outside world is essentially unknown to it.

===================================================================================
Deferal of events:
Its is also possible to defer an event to the next state. If the current state knows that the current event may be relavant in one of the next states it might make sense to defer it to be handled after the next transition. Whenever a transition takes place, the events in the deferal queue are processed in FIFO order by the state machine before processing any new events. As a real life analogy, in many cameras, if user clicks while the camera is still trying to set focus, the software does nothing at the moment but automatically takes a shot as soons as the focus is set.
So the "click" event was deferred while in "Focussing" state as it was relavant in the next "Focussed" state and was eventually processed.

To achieve this, the event handler must return SpecialEvents.defer in the respective Event handler to defer an event to the next state.

===================================================================================
Examples:
Please refer to the example code snippets in the "examples" directory to see coding examples.

