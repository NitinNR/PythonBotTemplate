import sched
import time

class MySched:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.instance, cls):
            print("New instance")
            cls.instance = super(MySched, cls).__new__(cls)
            cls.scheduler = sched.scheduler(time.time, time.sleep)
        else:
            print("No new instance")
        return cls.instance

    @property
    def scheduler(self):
        return self.scheduler

    # def cancelSched(self,schedId):
    #     self.scheduler.can