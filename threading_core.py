import os
import datetime
import queue
import threading
import time
import datetime_functions

class Job:
    def __init__(self,process,launch_time="now",periodicity=0):
        #process = "python test.py"
        self.process = process
        self.launch_time = launch_time
        self.periodicity = periodicity
        self.running = False   
        
    def run(self):
        self.running = True
        print(self.periodicity)
        if type(self.process)==str: #external process
            if self.periodicity==0:
                os.system("start cmd.exe @cmd /k "+self.process)
            else:
                while (self.running):
                    os.system("start cmd.exe @cmd /k "+self.process)
                    time.sleep(self.periodicity)     
        else:
            if self.periodicity==0:
                self.process()
            else:
                while (self.running):
                    self.process()
                    time.sleep(self.periodicity)               

class ThreadingCore:
    def __init__(self,dogui=None):
        self.jobs=[]
        self.queue_lock = threading.Lock()
        self.work_queue = queue.Queue(50)
        self.threads = []
        self.threadID = 1 #incremented from functions
        self.exit_flags_dict={}
        self.start_time = datetime.datetime.now()
        self.done=False
        self.dogui=dogui
                
    def process_data(self,thread,threadName, q):
        while not self.exit_flags_dict[thread.threadID]:
            self.queue_lock.acquire()
            if not self.work_queue.empty():
                data = q.get()
                self.queue_lock.release()
                print("%s processing %s" % (threadName, data))
            else:
                self.queue_lock.release()
            time.sleep(3)
                        
    def create_new_processing_thread(self,name,work_queue,threadID):
        thread = ProcessingThread(threadID, name, work_queue,self)
        thread.start()
        self.threads.append(thread)
        self.exit_flags_dict[self.threadID]=0
        self.threadID += 1        

    def create_new_time_thread(self,name,work_queue,threadID,refresh_period=1):
        thread = TimeThread(threadID, name, work_queue,self,refresh_period)
        thread.start()
        self.threads.append(thread)
        self.exit_flags_dict[self.threadID]=0
        self.threadID += 1
                
    def compute_time(self,thread):
        while not self.exit_flags_dict[thread.threadID]==1:
            current_time =  datetime.datetime.now()
            elapsed_time = current_time-self.start_time
            elapsed_seconds=round(elapsed_time.total_seconds())
            for job in self.jobs:
                if not(job.running):
                    if job.launch_time=="now":
                        job.run()
                    elif ":" in job.launch_time:
                        start=datetime_functions.convert_sql_date_and_time(job.launch_time)
                        if current_time.timestamp()>start:
                            job.run()
                    else:
                        if elapsed_seconds>=job.launch_time:
                            job.run()                                               
            time.sleep(thread.refresh_period)
            if self.dogui is not None and self.exit_flags_dict[thread.threadID]!=1:
                self.dogui.function()
            
    def exit_thread(self,thread_id):
        self.exit_flags_dict[thread_id]=1
        for t in self.threads:
            if t.threadID==thread_id:
                t.join()
        print(self.exit_flags_dict)

    def exit_all_threads(self):
       # Notify threads it's time to exit
        #exitFlag = 1
        for thread in self.threads:
            self.exit_flags_dict[thread.threadID]=1
            
        # Wait for all threads to complete
        for t in self.threads:
           print(self.exit_flags_dict)
           t.join()
        print("Exiting Main Thread")
        self.done=True
        


class SimpleThread (threading.Thread):
   def __init__(self, threadID, name, q, threading_core):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
      self.threading_core=threading_core #reference on the threading core

class ProcessingThread(SimpleThread):
    def __init__(self,threadID,name,q,threading_core):
        super().__init__(threadID,name,q,threading_core)

    def run(self):
        print("Starting " + self.name)
        self.threading_core.process_data(self,self.name, self.q,)
        print("Exiting " + self.name)

class TimeThread(SimpleThread):
    def __init__(self,threadID,name,q,threading_core,refresh_period):
        super().__init__(threadID,name,q,threading_core)
        self.refresh_period=refresh_period
        
    def run(self):
        print("Starting " + self.name)
        self.threading_core.compute_time(self)
        print("Exiting " + self.name)  
        