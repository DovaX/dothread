import dogui.dogui_core as dg
import dothread.dothread_core as dth
import dothread.threading_core as tc
import datetime

def click():
    pass

def gui_stop_threading():
    tc.exit_all_threads()

       
def gui_refresh():
    current_time =  datetime.datetime.now()
    time_elapsed = current_time-tc.start_time
    try:
        label1.text.set(time_elapsed)
    except:
        print("Thread overloaded - could not update time")


gui1=dg.GUI()
gui1.function=gui_refresh

tc=tc.ThreadingCore(gui1)
tc.create_new_time_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID,refresh_period=1.0)


dg.Button(gui1.window,"Stop threading",gui_stop_threading,1,1)

label1=dg.Label(gui1.window,"",2,2)

gui1.build_gui()