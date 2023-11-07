from time import *
class HanoiEngine:
    def __init__(self,num_discs:int,):
        self.num_discs=num_discs
        self.reset()
        pass
    
    def setGui(self,gui):
        self.gui=gui

    def reset(self,):
        self.pegs=[list(range(self.num_discs,0,-1)),[],[]]
        self.flag=True
        self.hanoi=self.towerOfHanoi(self.num_discs,0,1,2)
        self.count=2**self.num_discs-1
        pass

    def run(self,):
        while self.flag and self.count:
            self.nextStep()
            sleep(0.5)
        pass

    def pauseAndResume(self,):
        self.flag ^= True
        self.run()
        pass

    def nextStep(self,):
        if self.count==0: self.reset()
        next(self.hanoi)
        self.count-=1
        print(*self.pegs,sep='\n')
        print('=========')
        pass

    def towerOfHanoi(self,n,src,aux,dst):
        if n==1:
            yield self.moveDisc(src,dst)
            return
        yield from self.towerOfHanoi(n-1,src,dst,aux)
        yield self.moveDisc(src,dst)
        yield from self.towerOfHanoi(n-1,aux,src,dst)

    def moveDisc(self,src,dst):
        self.pegs[dst].append(self.pegs[src].pop())
        self.gui.showDiscAnimation()
        pass

if __name__ == '__main__':
    pass