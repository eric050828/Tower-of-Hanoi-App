import threading
from tkinter import *
from time import *
flag=True
def run():
    i=0
    while True:
        input_event.wait()
        if not flag:
            stop_lock.acquire()
        # else:
        #     # stop_lock.release()
        print(i,number)
        i+=1
        sleep(0.1)

def stop():
    global flag
    flag^=True
    if flag:
        stop_lock.release()

def getInput(input_box):
    global number, input_event
    number=input_box.get()
    input_event=threading.Event()
    if not number:
        number=3
    else:
        input_event.set()

def threadRun():
    thread_run.start()

window=Tk()
thread_run=threading.Thread(target=run)
thread_stop=threading.Thread(target=stop)
stop_lock=threading.Lock()
run_btn=Button(window,text='run',command=threadRun).pack()
stop_btn=Button(window,text='pause/resume',command=stop).pack()
input_box=Entry(window)
input_box.pack()
thread_input=threading.Thread(target=getInput,args=(input_box,))
thread_input.start()
window.mainloop()