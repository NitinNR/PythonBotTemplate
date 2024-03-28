
import sys
sys.path.append('../utility')
from singletone.myscheduler import MySched as t1

def testfun(sec):
    print("called..for ",sec)
    



t1obj = t1()
t1obj.scheduler.enter(3, 1, testfun, ([3]))
t1obj.scheduler.enter(4, 2, testfun, ([4]))
print("okkk")
async def runnit():
    await t1obj.scheduler.run()
    
# t = 
print("okkk2")

events = t1obj.scheduler._queue
print(events)
while True:
    pass

exit()
class MySingleton:
    pass


ms1 = MySingleton()
ms2 = MySingleton()
print(ms1 is ms2)
# False




exit()
# import pymysql as db
# USER =  'lifeel'
# DB = 'lifeeldb' 
# PASSWORD = 'lifeel123'
# HOST = 'db4free.net'
# PORT = 3306
# conn = db.Connection(host=HOST, port=PORT, user=USER,passwd=PASSWORD, db=DB)
# conn.close()

import sched
import time

# Create a scheduler object
scheduler = sched.scheduler(time.time, time.sleep)

def my_function():
    print("Function executed!")
    # Schedule the function to be called again after 5 seconds
    # scheduler.enter(5, 1, my_function, ())
    
    

# Schedule the function to be called after 5 seconds
event_id = scheduler.enter(2, 1, my_function, ())
print(event_id)

# Run the scheduler
scheduler.run()

while True:
    pass


