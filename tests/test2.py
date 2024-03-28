import sys
sys.path.append('../utility')
from singletone.myscheduler import MySched as t1
t1obj = t1()
events = t1obj.scheduler._queue

print("List of Events:")
for event in events:
    print(event)
    print(len(events))
    
    # timestamp, event_id, priority, action, argument = event
    if(event.priority == 1):t1obj.scheduler.cancel();