import threading_core as tc
import time


tc1=tc.ThreadingCore()

tc1.create_new_time_thread("Thread-"+str(tc1.threadID),tc1.work_queue,tc1.threadID,refresh_period=1.0)
tc1.create_new_processing_thread("Thread-2", tc1.work_queue, tc1.threadID)



def do_task():
    print("A")
    print("B")
    print("C")


time.sleep(2)

#tc1.process_data(tc1.threads[1], "Thread-2", tc1.work_queue)

job_list = ["One", "Two", "Three", "Four", do_task]
tc1.queue_lock.acquire()
for job in job_list:
   tc1.work_queue.put(job)
tc1.queue_lock.release()




time.sleep(20)
tc1.exit_all_threads()

#thread time - refreshing
#thread process - tray_icon
#thread scraping - scraping thread