import datetime_functions
import datetime
import threading_core
# CLI - Command Line Interface
    
def cli_interface(tc): #tc ~ threading_core
    
    while not tc.done:
        a=input("\n1)Show running threads, 2)Run new thread, 3)Fill the queue, \n4)Wait till empty queue, 5)Exit threads, 6)Show time\nCommands: 'stop X' - stops thread X, 'job X' - runs process (-t datetime, -p periodicity)\n")
        if a=="1":
            print(tc.threads)
        if a=="2":
            tc.create_new_processing_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID)
            
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
            tc.exit_all_threads()
    
        if a=="6":
            current_time =  datetime.datetime.now()
            time_elapsed = current_time-tc.start_time
            bool1=datetime_functions.does_exceed_current_timestamp("2019-05-17 12:28")
            print("Start:",tc.start_time,"Now:",current_time,"Elapsed:",time_elapsed,bool1)

        if "stop" in a:
            thread_id=int(a.split("stop ")[1])
            tc.exit_thread(thread_id)
                    
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
            job1=threading_core.Job(process,launch_time,periodicity)
            tc.jobs.append(job1)
            
            

tc=threading_core.ThreadingCore()
tc.create_new_time_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID)
cli_interface(tc)