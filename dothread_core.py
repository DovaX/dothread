import time
import datetime
import os

#from dir_mng import *


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


#run_function_in_interval(10,run_process,"calc")


"""File management queue"""

def identity(inp):
    return(inp)

def process_file(file,function=identity,queue_dir="queue",suffix=".pdf"):
    """processes only files without spaces in name"""
    print("Processing file "+file)
    function(file)

    filename = file.split("\\")[-1]
    #print(prefix,"FILE")
    #move_file("",suffix,queue_dir,queue_dir+"\\processed",0)


    path="move "+queue_dir+"\\"+filename+" "+queue_dir+"\\processed\\"+filename
    os.system(path)  

def process_all_files(all_files,function=identity,queue_dir="queue",suffix=".pdf"):        
    for file in all_files:
        process_file(file,function,queue_dir,suffix)
    
#process_all_files("queue",suffix=".pdf")





#Temporary solution - todo - remove this part

import glob
import os


"""###################   BEGIN DIRECTORY MANAGEMENT   ######################"""
def get_files_in_directory(dir,suffix):
    """Returns list of .txt files in given directory"""
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))    
    DIRECTORY = os.path.join(SITE_ROOT, dir)
    files = glob.glob(DIRECTORY + '/*'+suffix, recursive=True)
    return(files)

def name_contains(s,files):
    """Returns list of files containing given string s in their name"""
    list1=[]
    for file in files:
        if s in file:
            list1.append(file)    
    return(list1) 


def rename_files():
    """NOT USED"""
    dir=".//XML//"
    files=os.listdir(dir)

    for file in files:
        #if ".xml" not in file:
        os.rename(dir+file,dir+file[:-12]+".xml")

def move_all_files(prefix,suffix,olddir,newdir): 
    
    files=get_files_in_directory(olddir,suffix)
    list1=name_contains(prefix,files)
    for file in list1:
        filename=file.split('\\'+olddir+'\\')[1]
        #filename=filename.replace(' ','_')
        path="move "+olddir+"\\"+filename+" "+newdir+"\\"+filename
        os.system(path)
        
def move_really_all_files(olddir,newdir):
    path="mv "+olddir+" "+newdir
    os.system(path)

def move_file(prefix,suffix,olddir,newdir,index):
    """processes only files without spaces in name"""
    files=get_files_in_directory(olddir,suffix)
    list1=name_contains(prefix,files)
    print(list1,index,"TEST")
    filename=list1[index]
	 #print(list1, olddir,newdir)
    filename=filename.split('\\'+olddir+'\\')[1]
    path="move "+olddir+"\\"+filename+" "+newdir+"\\"+filename
    os.system(path)      

def get_all_files_from_list_of_directories(list_of_directories,suffix):
    all_files=[]
    for directory in list_of_directories:
        files=get_files_in_directory(directory,suffix)
        all_files=all_files+files
    return(all_files)

def next_file_number(prefix,suffix,all_files):
    number=0
    #print(all_files)
    
    print(all_files)
    for file in all_files:
        
        if "-" in file:
            file=file.split("-")[0]+".txt"
        try:
            x=file.split(prefix)[1]
        except:
            x=file.replace(prefix,"")
        print(x)
        y=int(x.split(suffix)[0])
        print("next",x)
        number=y if y>number else number
    number=number+1      
    return(number)      

def get_filename(path):
    """not used"""
    return(path.split("\\")[-1])
           