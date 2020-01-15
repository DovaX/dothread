import os
import datetime
import queue
import threading
import time

def convert_sql_date_and_time(s):
    #s="2019-05-17 11:20"
    b=s.split(" ")    
    hours=int(b[1].split(":")[0])
    minutes=int(b[1].split(":")[1])    
    daytimestamp=(time.mktime(datetime.datetime.strptime(b[0], "%Y-%m-%d").timetuple()))    
    return(daytimestamp+60*minutes+60*60*hours)

def does_exceed_current_timestamp(s):
    time_stamp=time.time()        
    #print(convert_sql_date_and_time("2019-04-01 10:10"))
    condition = time_stamp>convert_sql_date_and_time(s)
    return(condition)

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
                
jobs=[]

thread_list = ["Thread-1", "Thread-2", "Thread-3"]

job_list = ["One", "Two", "Three", "Four", "Five"]
queue_lock = threading.Lock()
work_queue = queue.Queue(50)
threads = []
threadID = 1

exitFlag = 0

exit_flags_dict={}

class MyThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print("Starting " + self.name)
      process_data(self,self.name, self.q)
      print("Exiting " + self.name)

def process_data(thread,threadName, q):
    while not exit_flags_dict[thread.threadID]:
        queue_lock.acquire()
        if not work_queue.empty():
            data = q.get()
            queue_lock.release()
            print("%s processing %s" % (threadName, data))
        else:
            queue_lock.release()
        time.sleep(3)


class TimeThread(MyThread):
    def __init__(self,threadID,name,q):
        super().__init__(threadID,name,q)
        
    def run(self):
        print("Starting " + self.name)
        compute_time(self)
        print("Exiting " + self.name)  
        
def compute_time(thread):
    global threadID
    global jobs
    while not exit_flags_dict[thread.threadID]:
        current_time =  datetime.datetime.now()
        elapsed_time = current_time-start_time
        elapsed_seconds=round(elapsed_time.total_seconds())
        #print(elapsed_seconds)
        for job in jobs:
            if not(job.running):
                if job.launch_time=="now":
                    job.run()
                elif ":" in job.launch_time:
                    start=convert_sql_date_and_time(job.launch_time)
                    if current_time.timestamp()>start:
                        job.run()
                    
                
                else:
                    if elapsed_seconds>=job.launch_time:
                        job.run()
                
                
                
        if elapsed_seconds==20:
            create_new_thread("Thread-"+str(threadID),work_queue,threadID)
            exit_flags_dict[threadID]=0
            threadID += 1        
        time.sleep(5)

def create_new_thread(name,work_queue,threadID):
   thread = MyThread(threadID, name, work_queue)
   thread.start()
   threads.append(thread)

def create_new_time_thread(name,work_queue,threadID):
   thread = TimeThread(threadID, name, work_queue)
   thread.start()
   threads.append(thread)

start_time = datetime.datetime.now()
done=False
create_new_time_thread("Thread-"+str(threadID),work_queue,threadID)
exit_flags_dict[threadID]=0
threadID += 1

while not done:
    a=input("1)Show running threads, 2)Run new thread, 3)Fill the queue, 4)Wait till empty queue, 5)Exit threads\n")
    if a=="1":
        print(threads)
    if a=="2":
        create_new_thread("Thread-"+str(threadID),work_queue,threadID)
        exit_flags_dict[threadID]=0
        threadID += 1
        
    if a=="3":
        # Fill the queue
        queue_lock.acquire()
        for job in job_list:
           work_queue.put(job)
        queue_lock.release()
    
    if a=="4":
        # Wait for queue to empty
        print(work_queue.empty())
        while not work_queue.empty():
           pass
       
    if a=="5":
        # Notify threads it's time to exit
        #exitFlag = 1
        for thread in threads:
            exit_flags_dict[thread.threadID]=1
            
        # Wait for all threads to complete
        for t in threads:
           t.join()
        print("Exiting Main Thread")
        done=True

    if a=="6":
        current_time =  datetime.datetime.now()
        time_elapsed = current_time-start_time
        bool1=does_exceed_current_timestamp("2019-05-17 12:28")
        print(start_time,current_time,time_elapsed,bool1)

    if "stop" in a:
        end_id=int(a.split("stop ")[1])
        exit_flags_dict[end_id]=1
        for t in threads:
            if t.threadID==end_id:
                t.join()
        print(exit_flags_dict)
        
        
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
        jobs.append(job1)