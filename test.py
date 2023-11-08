
from threading import Thread,Event as TEvent
from time import *
from HanoiEngine import HanoiEngine
from GUI import GUI
from tkinter import *
from random import randint
class Pegs:
    def __init__(self):
        self.reset()

    def reset(self,):
        self.width=10
        self.height=200
        self.pegs=[[],[],[]]
        self.hanoi=self.towerOfHanoi(num_discs,0,1,2)
        for index, number in enumerate(range(num_discs,0,-1)):
            disc=Disc(index,number)
            self.pegs[0].append(disc)
        for i in range(3):
            x0 = i * 200 + 200 - self.width // 2
            y0 = self.height
            x1 = x0 + self.width
            y1 = self.height*2
            peg=canvas.create_rectangle(x0, y0, x1, y1, fill='brown')
            canvas.tag_lower(peg)

    def moveDisc(self,src,dst):
        disc=self.pegs[src].pop()
        dst_x=dst*200+200-disc.width//2
        # disc.moveAnimation(dst_x-disc.x0,disc.index-len(self.pegs[dst]))
        disc.moveAnimation(dst_x,400-(len(self.pegs[dst])+1)*disc.height)
        disc.index=len(self.pegs[dst])
        self.pegs[dst].append(disc)
        
    
    def towerOfHanoi(self,n,src,aux,dst):
        if n==1:
            yield self.moveDisc(src,dst)
            return
        yield from self.towerOfHanoi(n-1,src,dst,aux)
        yield self.moveDisc(src,dst)
        yield from self.towerOfHanoi(n-1,aux,src,dst)


class Disc:
    def __init__(self,index,number):
        self.index=index
        self.number=number
        self.width=(number)*20
        self.height=10
        self.color="#{}{}{}".format(hex(randint(0,255))[2:].zfill(2),
                                    hex(randint(0,255))[2:].zfill(2),
                                    hex(randint(0,255))[2:].zfill(2))
        self.x0=200-self.width//2
        self.x1=self.x0+self.width
        self.y0=(-index - 1) * self.height+400
        self.y1=self.y0 + self.height
        self.drawDisc()
    def drawDisc(self,):
        self.rect=canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=self.color)
    
    def moveAnimation(self,dst_x,dst_y):
        # 向上
            while True:
                self.x0,self.y0,self.x1,self.y1=canvas.coords(self.rect)
                if self.y0 == 200-self.height*2: break
                canvas.move(self.rect,0,-1)
                sleep(speed/100)
        # 平移
            direct = 1 if self.x0<dst_x else -1  # 左或右
            while True:
                self.x0,self.y0,self.x1,self.y1=canvas.coords(self.rect)
                if self.x0 == dst_x: break
                canvas.move(self.rect,direct,0)
                sleep(speed/100)
        # 向下
            while True:
                self.x0,self.y0,self.x1,self.y1=canvas.coords(self.rect)
                if self.y0 == dst_y: break
                canvas.move(self.rect,0,1)
                sleep(speed/100)
        
    # def moveAnimation(self,delta_x,delta_y):
    #     canvas.move(self.rect,delta_x,delta_y*self.height)
    #     self.x0,self.y0,self.x1,self.y1=canvas.coords(self.rect)

class HanoiApp:
    def __init__(self, window):
        self.flag=True
        self.count=2**num_discs-1
        self.pegs=Pegs()
        self.run_btn = Button(frame,text='<Run>',command=self.run).grid(row=0, column=1)
        # self.pause_btn = Button(frame,text='<Pause/Resume>',command=self.stop).grid(row=1, column=1)
        self.next_btn = Button(frame,text='<Next Step>',command=self.nextStep).grid(row=2, column=1)
        # self.reset_btn = Button(frame,text='<Next Step>',command=self.).grid(row=2, column=1)
        self.run_event = TEvent()
        self.run_thread = Thread(target=self.runAll)

    def run(self,): 
        self.run_thread.start()    
        
    def stop(self):
        if not self.run_event.is_set():
            self.run_event.set()
        else:
            self.run_event.clear()
            self.runAll()

    def runAll(self):
        while self.flag and self.count and not self.run_event.is_set():
            self.nextStep()
            sleep(speed)
            
    def nextStep(self,):
        # if self.count==0: self.reset()
        next(self.pegs.hanoi)
        self.count-=1
        self.report()
        
    def report(self,):
        for p in self.pegs.pegs:
            print('[',end='')
            for disc in p:
                print(disc.number,end=' ')
            print(']')
        print('\n=========\n')

def main():
    global window, canvas, frame, num_discs, speed
    canvas_w=800
    canvas_h=400
    window_w=800
    window_h=600
    num_discs=3
    speed=1/8
    window = Tk()
    window.geometry('{}x{}'.format(window_w,window_h))
    canvas = Canvas(window,width=canvas_w,height=canvas_h,bg='white')
    canvas.pack()
    frame=Frame()
    frame.pack()
    app = HanoiApp(window)
    window.mainloop()


if __name__ == '__main__':
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
    main()