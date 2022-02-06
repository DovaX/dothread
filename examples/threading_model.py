import threading_core
import datetime
import sys
sys.path.append("C:\\Users\\EUROCOM\\Documents\\Git\\DovaX")

import dogui.dogui_core as dg

def gui_stop_threading():
    tc.exit_all_threads()

def gui_refresh():
    label1.text.set(tc.threads)
    current_time =  datetime.datetime.now()
    time_elapsed = current_time-tc.start_time
    label2.text.set(time_elapsed)

def gui_new_processing_thread():
    tc.create_new_processing_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID)

gui1=dg.GUI()
gui1.function=gui_refresh

tc=threading_core.ThreadingCore(gui1)
tc.create_new_time_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID)

label1=dg.Label(gui1.window,"",2,1)
label2=dg.Label(gui1.window,"",2,2)

dg.Button(gui1.window,"Stop threading",gui_stop_threading,1,1)
dg.Button(gui1.window,"Refresh",gui_refresh,1,2)
dg.Button(gui1.window,"New thread",gui_new_processing_thread,1,3)

gui1.build_gui()