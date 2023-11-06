from time import *
def display():
    print(*pegs,sep='\n')
    print('=========')

def moveDisc(src,dst):
    pegs[dst].append(pegs[src].pop())

def hanoi(n,src,aux,dst):
    if n==1:
        yield moveDisc(src,dst)
        
        return
    yield from hanoi(n-1,src,dst,aux)
    yield moveDisc(src,dst)
    yield from hanoi(n-1,aux,src,dst)

def reset(n):
    global pegs,stack
    pegs = [list(range(n,0,-1)),[],[]]
    stack=[(n,0,1,2)]

num_discs=int(input())
cmd=''
reset(num_discs)
hanoi_tower=hanoi(num_discs,0,1,2)
for _ in range(2**num_discs-1):
    # cmd=input()
    # if cmd=='q':break
    next(hanoi_tower)
    display()
    sleep(1)
    # flag=True

    # while stack and flag:
    #     n, src, aux, dst = stack.pop()
    #     if n == 1:
    #         moveDisc(src, dst)
    #         flag=False
    #     else:
    #         stack.append((n - 1, aux, src, dst))
    #         stack.append((1, src, aux, dst))
    #         stack.append((n - 1, src, dst, aux))