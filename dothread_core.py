import time
import datetime
import os


def run_function_in_interval(seconds,function,*args):
    now = datetime.datetime.now()
    interval=0
    while(True):    
        time.sleep(1)
        diff=datetime.datetime.now()-now
        print(diff)
        trigger = diff.seconds//seconds-interval
        if trigger == 1:
            function(args[0])
        interval = diff.seconds//seconds 
        
        
def run_process(*args):
    os.system(args[0])


run_function_in_interval(10,run_process,"calc")