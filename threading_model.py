import threading_core
import threading_cli
#import dogui.dogui_core as dg

tc=threading_core.ThreadingCore()
tc.create_new_time_thread("Thread-"+str(tc.threadID),tc.work_queue,tc.threadID)
threading_cli.cli_interface(tc)



"""
def gui_stop_threading():
    threading_cli.exit_all_threads(tc)


def gui_refresh():
    label1.text.set(tc.threads)


gui1=dg.GUI()



label1=dg.Label(gui1.window,"",2,1)

dg.Button(gui1.window,"Stop threading",gui_stop_threading,1,1)
dg.Button(gui1.window,"Refresh",gui_refresh,1,2)


gui1.build_gui()
"""


#while not tc.done:
#    pass