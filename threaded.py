from tkinter import ttk
from tkinter import *
import os
from tkinter import messagebox as m_box
import re
import requests
import threading
import time


n=15


histroy = dict()
def part_downloader(start,end,url,filename):

    file_headers = {'Range':'bytes=%d-%d'%(start,end)}

    r = requests.get(url,headers=file_headers,stream=True)

    with open(filename,"r+b") as fp:
        fp.seek(start)
        fp.write(r.content)


def download(url,thread_count):

    r = requests.head(url)
    filename =file_name_bfr_click.get()
    if(len(filename) == 0):
        filename = str(str(url).split('/')[-1])
    print("called download for ",filename)
    try:
        size = int(r.headers['content-length'])
        print("File size recieved is ",str(size/1024)," KB")
    except:
        print("Invalid url or File cannot be downloaded")
        return
    try:
        if histroy[filename] is 'downloading':
            print("File %s is already being downloaded"%(filename))
            return
    except:
        histroy[filename] = 'downloading'
    fraction = int(size/int(thread_count))
    
    with open(filename,"w") as fp:
        fp.write("\0" * size)
        fp.close
    
    start_time = time.time()

    threadlist = list()
    for i in range(int(thread_count)):
        start = i*fraction
        end = start + fraction

        t = threading.Thread(target=part_downloader,kwargs={'start':start,'end':end,'url':url,'filename':filename})
        # t.setDaemon(True)
        t.start()
        threadlist.append(t)
        

    for t in threadlist:
        t.join()
    histroy[filename] = 'downloaded'

    print("file " + str(filename)+" size = "+str(size/(1024))+"kb threads used "+str(thread_count)+ " downloaded time taken = " + str(round(time.time()-start_time,3)) +"s")

#runner is here 
def onClick() :
        file_url = url.get()
        download(file_url,n)


def newThread():
    t = threading.Thread(target =onClick)
    t.start()

def Exit():
    print("Exiting...")
    win.destroy()
    sys.exit()

win = Tk()
win.title("Welcome to FAST Downloader")
bgimage = PhotoImage(file ="new.png")
Label(win,image=bgimage).place(relwidth=1,relheight=1)
win.geometry("500x360")
win.minsize(500,360)
win.maxsize(500,360)
frame = ttk.LabelFrame(win, width=290)
frame.pack(padx=30, pady=90)
label1 = ttk.Label(frame, text="Enter The File URL : ")
label1.grid(row=0, column=0,sticky=W)
url = StringVar()
edit_txt = ttk.Entry(frame, width=50, textvariable=url)
edit_txt.grid(row=1, columnspan=4, padx=2, pady=3)
label2 = ttk.Label(frame, text="Enter The File Name : ")
label2.grid(row=2, column=0,sticky=W)
file_name_bfr_click = StringVar()
file_name = ttk.Entry(frame, width=50, textvariable=file_name_bfr_click)
file_name.grid(row=3, columnspan=4, padx=2, pady=3)

btn1 = ttk.Button(frame, width=30, text="Download File", command=newThread)
btn1.grid(row=4,column=0)

ExitB = Button(frame,text='Exit',command = Exit)
ExitB.grid(row=4,column=1)


win.mainloop()
