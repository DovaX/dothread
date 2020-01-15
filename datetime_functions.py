#imported by dothread.control_thread
import datetime
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