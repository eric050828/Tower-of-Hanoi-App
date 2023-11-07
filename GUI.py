from tkinter import *
class GUI:
    def __init__(self,window,num_discs,hanoi_engine):
        self.hanoi_engine=hanoi_engine
        self.discs=self.hanoi_engine.pegs
        self.interface_config={
            'window':window,
            'num_discs':num_discs,
            'canvas_w':600,
            'canvas_h':400,
            'window_w':800,
            'window_h':600,
        }
        self.initInterface(**self.interface_config)
        self.peg_config={
            'width':10,
            'height':200,
        }
        self.drawPegs(**self.peg_config)
        self.disc_config={
            'width':30,
            'height':10,
        }
        self.drawDiscs(**self.disc_config)
        self.initButtons()
        pass

    def initInterface(self,window,num_discs,canvas_w,canvas_h,window_w,window_h):
        self.window = window
        self.window.geometry('{}x{}'.format(window_w,window_h))
        self.canvas = Canvas(self.window,width=canvas_w,height=canvas_h,bg='white')
        self.canvas.pack()
        self.frame=Frame()
        self.frame.pack()
        self.num_discs = num_discs
        pass

    def initButtons(self,):
        self.input_number = Entry(self.frame).grid(row=0,column=0)
        self.run_btn = Button(self.frame,text='<Run>',command=self.hanoi_engine.run).grid(row=0, column=1)
        self.pause_btn = Button(self.frame,text='<Pause/Resume>',command=self.hanoi_engine.pauseAndResume,default='active').grid(row=1, column=1)
        self.next_btn = Button(self.frame,text='<Next Step>',command=self.hanoi_engine.nextStep).grid(row=2, column=1)
        self.reset_btn=Button(self.frame,text='<Reset>',command=self.hanoi_engine.reset).grid(row=3, column=1)
        
    
    def drawPegs(self,width,height):
        for i in range(3):
            x0 = i * 200 + 100 - width // 2
            y0 = height
            x1 = x0 + width
            y1 = 400
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='brown')
        pass
    
    def drawDiscs(self,width,height):
        for i in range(self.num_discs):
            disc = self.canvas.create_rectangle(0, 0, 0, 0, fill="")
            self.discs.append(disc)

    def showDiscAnimation(self,):
        pass


if __name__ == '__main__':
    pass