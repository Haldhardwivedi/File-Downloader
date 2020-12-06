from tkinter import *
import requests
import threading
import time

# n is the number of threads being used
n=15

#history stores the state of files 
#being downloaded or downloading
history = dict()

#part_downloader function accepts the start 
# and end byte index
def part_downloader(start,end,url,filename):

    #file_headers contains dictionary with 
    #the range of the bytes specified to be downloaded
    file_headers = {'Range':'bytes=%d-%d'%(start,end)}
    
    #request to get the response object  
    #with specified headers
    r = requests.get(url,headers=file_headers,stream=True)

    #open the file for reading and writing in binary mode
    with open(filename,"r+b") as fp:
        #goto the required positon with seek 
        fp.seek(start)
        #dump  the contents of the file in the file
        fp.write(r.content)


def download(url,thread_count):

    #send a head request to the url and save it 
    # in r which is the response object
    r = requests.head(url) 

    filename =file_name_bfr_click.get()
    #get the filename from filename entry widget
    #if the filename entry widget was left empty
    #  then use the default name of file 
    if(len(filename) == 0):
        filename = str(str(url).split('/')[-1])
    print("called download for",filename,"from",url)

    #from the headers get the content-length 
    try:
        size = int(r.headers['content-length'])
        print("File size recieved is ",str(round(size/1024,3))," KB")
    except:
        print("Invalid url or File cannot be downloaded")
        return
    #check if we are not downloading the same file under the same name 
    #so that we dont have any conflicts 
    try:
        if history[filename] == 'downloading':
            print("File %s is already being downloaded"%(filename))
            return
    except:
        history[filename] = 'downloading'
    
    #calculate the fraction of bytes which we need for each thread
    fraction = int(size/int(thread_count))

    #create file and write empty characters in each and every 
    #byte for the required size
    with open(filename,"w") as fp:
        fp.write("\0" * size)
        fp.close
    
    start_time = time.time()

    #create list for holding the threads which we created
    threadlist = list()

    #create threads for downloading the parts of the file
    for i in range(int(thread_count)):

        start = i*fraction
        end = start + fraction
        #create thread with part_downloader function and 
        #give the url and the parameters for the file headers to download
        t = threading.Thread(target=part_downloader,
        kwargs={'start':start,'end':end,'url':url,'filename':filename})
        t.start()
        threadlist.append(t)
        
    #wait for all threads to finish
    for t in threadlist:
        t.join()
    #marks the file as downloaded
    history[filename] = 'downloaded'

    print("file " + str(filename)+" size = "+str(size/(1024))+"kb threads used",
    str(thread_count)+ " downloaded time taken =",
    str(round(time.time()-start_time,3)),"s")

#runner is here 
#get the url from entry and give it to download function
#with the number of threads as n
def runner_download() :
        file_url = url.get()
        download(file_url,n)

#when clicking the download button create
#new thread and call the runner download function
def onClick():
    t = threading.Thread(target =runner_download)
    t.start()

#function for exiting the program
def Exit():
    print("Exiting...")
    win.destroy()
    sys.exit()

#Create the main frame
win = Tk()
win.title("Welcome to FAST Downloader")
bgimage = PhotoImage(file ="new.png")
Label(win,image=bgimage).place(relwidth=1,relheight=1)
win.geometry("500x360")
win.minsize(500,360)
win.maxsize(500,360)

#Create inner Frame for inputs and button
frame = LabelFrame(win, width=290)
frame.pack(padx=30, pady=90)

urlLB = Label(frame, text="Enter The File URL : ")
urlLB.grid(row=0, column=0,sticky=W)
url = StringVar()
#Entry widget for url
url_entry = Entry(frame, width=50, textvariable=url)
url_entry.grid(row=1, columnspan=4, padx=2, pady=3)

fileNameLB = Label(frame, text="Enter The File Name : ")
fileNameLB.grid(row=2, column=0,sticky=W)

file_name_bfr_click = StringVar()
file_name = Entry(frame, width=50, textvariable=file_name_bfr_click)
file_name.grid(row=3, columnspan=4, padx=2, pady=3)
#Create Download Button with command newThread which creates
# new thread and starts downloading the file from url
DownloadBT = Button(frame, width=30, text="Download File", command=onClick)
DownloadBT.grid(row=4,column=0)

#Button for Exiting the application
ExitB = Button(frame,text='Exit',command = Exit)
ExitB.grid(row=4,column=1)


win.mainloop()
