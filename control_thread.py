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
        if self.periodicity==0:
            os.system("start cmd.exe @cmd /k "+self.process)
        else:
            while (self.running):
                os.system("start cmd.exe @cmd /k "+self.process)
                time.sleep(self.periodicity)                

class ThreadingCore:
    def __init__(self):
        self.jobs=[]
        self.queue_lock = threading.Lock()
        self.work_queue = queue.Queue(50)
        self.threads = []
        self.threadID = 1 #incremented from functions
        self.exit_flags_dict={}
        
    def initialize_threading_core(self):
        self.start_time = datetime.datetime.now()
        self.done=False
        self.create_new_time_thread("Thread-"+str(self.threadID),self.work_queue,self.threadID)
        self.exit_flags_dict[self.threadID]=0
        self.threadID += 1
        
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

    def create_new_time_thread(self,name,work_queue,threadID):
        thread = TimeThread(threadID, name, work_queue,self)
        thread.start()
        self.threads.append(thread)
        
        
    def compute_time(self,thread):
        while not self.exit_flags_dict[thread.threadID]:
            current_time =  datetime.datetime.now()
            elapsed_time = current_time-self.start_time
            elapsed_seconds=round(elapsed_time.total_seconds())
            #print(elapsed_seconds)
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
            if elapsed_seconds==20:
                self.create_new_processing_thread("Thread-"+str(self.threadID),self.work_queue,self.threadID)
                self.exit_flags_dict[self.threadID]=0
                self.threadID += 1        
            time.sleep(5)

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
    def __init__(self,threadID,name,q,threading_core):
        super().__init__(threadID,name,q,threading_core)
        
    def run(self):
        print("Starting " + self.name)
        self.threading_core.compute_time(self)
        print("Exiting " + self.name)  
        
# CLI - Command Line Interface
def cli_interface(tc): #tc ~ threading_core
    
    while not tc.done:
        a=input("\n1)Show running threads, 2)Run new thread, 3)Fill the queue, \n4)Wait till empty queue, 5)Exit threads, 6)Show time\nCommands: 'stop X' - stops thread X, 'job X' - runs process (-t datetime, -p periodicity)\n")
        if a=="1":
            print(tc.threads)
        if a=="2":
            tc.create_new_processing_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID)
            tc.exit_flags_dict[tc.threadID]=0
            tc.threadID += 1
            
        if a=="3":
            # Fill the queue
            job_list = ["One", "Two", "Three", "Four", "Five"]
            tc.queue_lock.acquire()
            for job in job_list:
               tc.work_queue.put(job)
            tc.queue_lock.release()
        
        if a=="4":
            # Wait for queue to empty
            print(tc.work_queue.empty())
            while not tc.work_queue.empty():
               pass
           
        if a=="5":
            # Notify threads it's time to exit
            #exitFlag = 1
            for thread in tc.threads:
                tc.exit_flags_dict[thread.threadID]=1
                
            # Wait for all threads to complete
            for t in tc.threads:
               t.join()
            print("Exiting Main Thread")
            tc.done=True
    
        if a=="6":
            current_time =  datetime.datetime.now()
            time_elapsed = current_time-tc.start_time
            bool1=datetime_functions.does_exceed_current_timestamp("2019-05-17 12:28")
            print("Start:",tc.start_time,"Now:",current_time,"Elapsed:",time_elapsed,bool1)
    
        if "stop" in a:
            end_id=int(a.split("stop ")[1])
            tc.exit_flags_dict[end_id]=1
            for t in tc.threads:
                if t.threadID==end_id:
                    t.join()
            print(tc.exit_flags_dict)
                    
        if "job" in a:
            launch_time = "now"
            periodicity = 0
            if " -p " in a:
                periodicity=int(a.split(" -p ")[1])
                #in seconds
                a=a.split(" -p ")[0]
            
            if " -t " in a:
                launch_time=a.split(" -t ")[1]
                a=a.split(" -t ")[0]
            process = a.split("job ")[1]        
            job1=Job(process,launch_time,periodicity)
            tc.jobs.append(job1)


threading_core=ThreadingCore()
threading_core.initialize_threading_core()
cli_interface(threading_core)
