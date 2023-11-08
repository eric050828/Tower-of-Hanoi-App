"""
2023/11/08
NTUST MIS
B11209024 李O穎
Tower of Hanoi App
"""
from tkinter import *
from threading import *
from random import randint
from time import sleep

# Core Engine
def towerOfHanoi(n:int, src:int, aux:int, dst:int):
    if n==1:
        yield moveDisc(src,dst)
        event_animation_finished.wait()
        return
    # event_animation_finished.clear()
    yield from towerOfHanoi(n-1,src,dst,aux)
    yield moveDisc(src,dst)
    event_animation_finished.wait()
    yield from towerOfHanoi(n-1,aux,src,dst)

# move disc from src to dst
def moveDisc(src:int, dst:int):
    event_animation_finished.wait()
    event_animation_finished.clear()
    index, number, rect = pegs[src].pop()
    x0, _, x1, _ = getPegPosition(dst)  # get x
    _, y0, _, y1 = getDiscPosition(len(pegs[dst])+1, number,dst)
    # moveAnimation(index, rect, [x0, y0, x1,y1])
    thread_animation = Thread(target=moveAnimation, args=(index, number, rect, [x0, y0, x1,y1], ))
    thread_animation.start()
    index = len(pegs[dst])
    pegs[dst].append((index, number, rect))
    pass

# show the movement animation
def moveAnimation(index, number, rect, dst:list[int]):
    # event_animation_finished.clear()
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
    pass

def threadRun():
    # thread_run.start()
    thread_run = Thread(target=run)
    thread_run.start()
    pass

def run():
    while not event_pause.is_set():
        btn_run.config(state=DISABLED)
        btn_next.config(state=DISABLED)
        btn_reset.config(state=DISABLED)
        nextStep()
        sleep(speed)

def pauseAndResume():
    if event_pause.is_set():
        event_pause.clear()
        btn_run.config(state=NORMAL)
    else:
        event_pause.set()
        btn_run.config(state=DISABLED)
        btn_next.config(state=NORMAL)
        btn_reset.config(state=NORMAL)

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
    speed = 1/getSpeed()
    hanoi = towerOfHanoi(num_discs,0,1,2)
    event_animation_finished.set()
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
    print(current_thread())

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
    return int(speed_box.get())

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

def drawDiscs():
    for i in range(num_discs):  # 小 -> 大 , 上 -> 下
        color = "#" + "".join([hex(randint(0, 255))[2:].zfill(2) for j in range(3)])
        x0, y0, x1, y1 = getDiscPosition(i, (num_discs-i), 0)
        rect = canvas.create_rectangle(x0,y0,x1,y1, fill=color)
        pegs[0].append((i,(num_discs-i),rect))
    pass

# window
window_width = 1200
window_height = 600
window = Tk()
window.geometry('%dx%d'%(window_width,window_height))

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
num_box = Entry(frame, width=box_width)
num_box.grid(row=0, column=0)
speed_box = Entry(frame, width=box_width)
speed_box.grid(row=1, column=0)
btn_run = Button(frame, text= "<Run!>", width=button_width, height=button_height, command=threadRun)
btn_run.grid(row=0, column=1)
btn_pause = Button(frame, text= "<Pause/Resume>", width=button_width, height=button_height, command=pauseAndResume)
btn_pause.grid(row=1, column=1)
btn_next = Button(frame, text= "<Next>", width=button_width, height=button_height, command=nextStep)
btn_next.grid(row=2, column=1)
btn_reset = Button(frame, text= "<Reset>", width=button_width, height=button_height, command=reset)
btn_reset.grid(row=3, column=1)

# pegs
peg_width = 10
peg_height = 200
peg_margin = 200
pegs = [[], [], []]
drawPegs()

# discs
default_num_discs = 3
num_discs = getDiscNum()
disc_width = 20
disc_height = 10
drawDiscs()

# hanoi logic
move_count = 2 ** num_discs - 1
default_speed = 10
speed = 1/getSpeed()
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