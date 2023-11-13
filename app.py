"""
2023/11/08
NTUST MIS
Create by:李丞穎
Tower of Hanoi App
source:https://github.com/eric050828/Tower-of-Hanoi-App
"""
from tkinter import Tk, DISABLED, NORMAL, StringVar, Entry, Button, Canvas, Frame, Label, RIGHT
from threading import Thread
from threading import Event
from threading import  enumerate as Tenumerate

from random import randint
from time import sleep
from sys import exit
import colorsys
# Core Engine
def towerOfHanoi(n:int, src:int, aux:int, dst:int):
    if n==1:
        yield moveDisc(src,dst)
        return
    yield from towerOfHanoi(n-1,src,dst,aux)
    yield moveDisc(src,dst)
    yield from towerOfHanoi(n-1,aux,src,dst)

# move disc from src to dst
def moveDisc(src:int, dst:int):
    index, number, rect = pegs[src].pop()
    x0, _, x1, _ = getPegPosition(dst)  # get x
    _, y0, _, y1 = getDiscPosition(len(pegs[dst])+1, number,dst)
    moveAnimation(index, number, rect, [x0, y0, x1,y1])
    index = len(pegs[dst])
    pegs[dst].append((index, number, rect))
    pass

# show the movement animation
def moveAnimation(index, number, rect, dst:list[int]):
    #event_animation_finished.clear()
    # 向上
    while True:
        x0,y0,x1,y1=canvas.coords(rect)
        if y0 == canvas_height-peg_height - 2*disc_height: break
        canvas.move(rect,0,-1)
        sleep(speed/100)
    # 平移
    direct = 1 if x0 < dst[0] else -1  # 向左或向右
    while True:
        x0,y0,x1,y1=canvas.coords(rect)
        if x0 == dst[0] + peg_width//2 - getDiscWidth(number)//2: break
        canvas.move(rect,direct,0)
        sleep(speed/100)
    # 向下
    while True:
        x0,y0,x1,y1=canvas.coords(rect)
        if y0 == dst[3]: break
        canvas.move(rect,0,1)
        sleep(speed/100)
    event_animation_finished.set()

def threadRun():
    thread_run = Thread(target=run)
    thread_run.start()
    pass

def run():
    thread_next = Thread(target=runSteps)
    thread_next.start()

def pauseAndResume():
    if event_pause.is_set():
        btn_run.config(state=NORMAL)
        event_pause.clear()
    else:
        event_pause.set()
        btn_run.config(state=DISABLED)
        btn_next.config(state=NORMAL)
        btn_reset.config(state=NORMAL)

def runSteps():
    try:
        if not event_pause.is_set():
            btn_run.config(state=DISABLED)
            btn_next.config(state=DISABLED)
            btn_reset.config(state=DISABLED)
            next(hanoi)
            report()
            thread_next = Thread(target=runSteps)
            thread_next.start()
    except StopIteration:
        finish()

def threadNext():
    thread_next = Thread(target=nextStep)
    thread_next.start()


def nextStep():
    try:
        next(hanoi)
        report()
    except StopIteration:
        event_finished.set()

def reset():
    global pegs, num_discs, speed, hanoi
    canvas.delete(*canvas.find_all())
    btn_run.config(state=NORMAL)
    btn_pause.config(state=NORMAL)
    btn_next.config(state=NORMAL)
    pegs = [[], [], []]
    drawPegs()
    num_discs = getDiscNum()
    drawDiscs()
    speed = 1/(getSpeed()*10)
    hanoi = towerOfHanoi(num_discs,0,1,2)
    event_pause.clear()
    event_finished.clear()
    pass

def finish():
    event_finished.wait()
    btn_run.config(state=DISABLED)
    btn_pause.config(state=DISABLED)
    btn_next.config(state=DISABLED)
    btn_reset.config(state=NORMAL)
    event_finished.clear()

def report():
    for peg in pegs:
        print(list(map(lambda x:x[1], peg)))
    print('='*20)
    # print(current_thread())

def getPegPosition(index:int):
    x0 = 200 + index*peg_margin*2 - peg_width//2
    x1 = x0 + peg_width
    y0 = canvas_height
    y1 = canvas_height - peg_height
    return [x0, y0, x1, y1]

def drawPegs():
    for i in range(3):
        x0, y0, x1, y1 = getPegPosition(i)
        peg = canvas.create_rectangle(x0, y0, x1, y1, fill='brown')
        canvas.tag_lower(peg)
    pass

def getDiscNum():
    if not num_box.get():
        return default_num_discs
    return int(num_box.get())

def getSpeed():
    if not speed_box.get():
        return default_speed
    return eval(speed_box.get())

def getDiscWidth(number:int):
    return number * disc_width

def getDiscPosition(index:int,number:int, peg:int):
    width = getDiscWidth(number)  # index越大 -> width越窄
    peg_x0, _, _, _ = getPegPosition(peg)
    x0 = peg_x0+peg_width//2 - width//2
    x1 = x0 + width
    y0 = canvas_height - (index+1) * disc_height  # index越大 -> 位置越高
    y1 = y0 + disc_height
    return [x0, y0, x1, y1]

colors = [colorsys.hsv_to_rgb(i / num_discs, 1, 1) for i in range(num_discs)]
def drawDiscs():
    for i in range(num_discs):  # 小 -> 大 , 上 -> 下
        # color = "#" + "".join([hex(randint(0, 255))[2:].zfill(2) for j in range(3)])
        color = '#%02X%02X%02X' % tuple(int(c * 255) for c in colors[i])
        x0, y0, x1, y1 = getDiscPosition(i, (num_discs-i), 0)
        rect = canvas.create_rectangle(x0,y0,x1,y1, fill=color)
        pegs[0].append((i,(num_discs-i),rect))
    pass

# window
window_width = 1200
window_height = 600
window = Tk()
window.geometry('%dx%d'%(window_width,window_height))
window.title('Tower of Hanoi App')

# interface
canvas_width = window_width
canvas_height = 400
canvas = Canvas(window, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()
frame = Frame(window)
frame.pack()

# buttons
button_width = 20
button_height = 1
box_width = 20

default_num_discs = "3"
num_label = Label(frame, text='圓盤數量(建議1-16):')
num_label.grid(row=0, column=0)
num_box = Entry(frame, width=box_width,textvariable=StringVar(value=default_num_discs))
num_box.grid(row=0, column=1)

default_speed = "1"
speed_label = Label(frame, text="圓盤移動速度(建議1-10):", justify=RIGHT)
speed_label.grid(row=1, column=0)
speed_box = Entry(frame, width=box_width,textvariable=StringVar(value=default_speed))
speed_box.grid(row=1, column=1, rowspan=2)

btn_run = Button(frame, text= "<Run!>", width=button_width, height=button_height, command=run, pady=10)
btn_run.grid(row=0, column=2, rowspan=2)

btn_pause = Button(frame, text= "<Pause/Resume>", width=button_width, height=button_height, command=pauseAndResume, pady=10)
btn_pause.grid(row=0, column=3, rowspan=2)

btn_next = Button(frame, text= "<Next>", width=button_width, height=button_height, command=threadNext, pady=10)
btn_next.grid(row=0, column=4, rowspan=2)

btn_reset = Button(frame, text= "<Reset>", width=button_width, height=button_height, command=reset, pady=10)
btn_reset.grid(row=0, column=5, rowspan=2)
btn_reset = Button(frame, text= "<Quit>", width=button_width, height=button_height, command=exit, pady=10)
btn_reset.grid(row=0, column=6, rowspan=2)

# pegs
peg_width = 10
peg_height = 200
peg_margin = 200
pegs = [[], [], []]
drawPegs()

# discs
num_discs = getDiscNum()
disc_width = 20
disc_height = 10
drawDiscs()

# hanoi logic
move_count = 2 ** num_discs - 1
speed = 1/(getSpeed()*10)
hanoi = towerOfHanoi(num_discs,0,1,2)

# threadings
# thread_animation = Thread(target=moveAnimation)
# thread_run = Thread(target=run)
event_animation_finished = Event()
event_animation_finished.set()
event_pause = Event()
event_finished = Event()

def main():
    window.mainloop()
    pass

if __name__ == "__main__":
    main()