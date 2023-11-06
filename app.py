from tkinter import *

class HanoiEngine:
    def __init__(self):
        self.disc_number=3
        self.colors=['red','yellow','green']
    def setDiscNumber(self,n):
        self.disc_number=n
    
    def moveDisc(self,src,dst):
        pass
    
    def hanoi(self,n,src,aux,dst):
        if n==1:
            self.moveDisc(src,dst)
            return
        self.hanoi(n-1,src,dst,aux)
        yield None
        self.moveDisc(src,dst)
        self.hanoi(n-1,aux,src,dst)
        yield None

class GUI:
    def __init__(self,window):
        self.window=window
        self.hanoi_engine=HanoiEngine()
        self.window.geometry('800x400')
        self.window.resizable(False,False)
        self.canvas = Canvas(window,width=600,height=300,bg='#1A1A1A')
        self.canvas.pack()
        self.frame = Frame(window)
        self.frame.pack()
        self.peg_width = 10
        self.peg_height = 200
        self.disc_width = 30
        self.disc_height = 10
        self.num_discs=3
        self.discs = []
        self.setPegs()
        self.setDiscs()
        pass
    

    def setPegs(self,):
        for i in range(3):
            x0 = i * 200 + 100 - self.peg_width // 2
            y0 = self.peg_height
            x1 = x0 + self.peg_width
            y1 = 400
            self.canvas.create_rectangle(x0, y0, x1, y1, fill='brown')
    def setDiscs(self):
        for i in range(self.num_discs):
            disc = self.canvas.create_rectangle(0, 0, 0, 0, fill=self.hanoi_engine.colors[i % 3])
            self.discs.append(disc)

class HanoiApp:
    def __init__(self,window):
        self.window = window
        self.gui = GUI(self.window)
        self.hanoi_engine=HanoiEngine()
        self.setButtons()

    def setButtons(self,):
        self.input_number = Entry(self.gui.frame).grid(row=0,column=0)
        self.start_btn = Button(self.gui.frame,text='<Start>',command=self.start).grid(row=0, column=1)
        self.stop_btn = Button(self.gui.frame,text='<Stop>',command=self.pause).grid(row=1, column=1)
        self.next_btn = Button(self.gui.frame,text='<Next Step>',command=self.nextStep).grid(row=2, column=1)
        pass

    def start(self,):
        print('start')
        return
    
    def pause(self,):
        print('pause')
        return
    
    def nextStep(self,):
        print('next')
        return
    


def main():
    window = Tk()
    app=HanoiApp(window)
    window.mainloop()
    return

if __name__=='__main__':
    main()