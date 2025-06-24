import random
import numpy as np
import math
import statistics

sdk = np.array([list(map(int,input().strip())) for _ in range (9)])

def PrintSudoku(sudoku):
    print("\n")
    for i in range(len(sudoku)):
        line = ""
        if i==3 or i==6:
            print ("-------------------")
        for j in range(len(sudoku[i])):
            if j==3 or j==6:
                line+="| "
            line+= str(sudoku[i,j])+" "
        print (line)

def FixedSudokuValues(fixedsdk):
    for i in range (0,9):
        for j in range (0,9):
            if fixedsdk[i,j]!=0:
                fixedsdk[i,j]=1
    return (fixedsdk)

def cost(sudoku):
    errors=0
    for i in range (0,9):
        errors+= costRowColumn(i,i,sudoku)
    return (errors)

def costRowColumn(row,col,sudoku):
    return (18-len(np.unique(sudoku[:,col]))-len(np.unique(sudoku[row,:])))

def createlistblocks():
    finallist=[]
    for r in range (0,9):
        tlist=[]
        block1=[i+3*(r%3) for i in range (0,3)]
        block2=[i+3*math.trunc(r/3) for i in range (0,3)]
        for x in block1:
            for y in block2:
                tlist.append([x,y])
        finallist.append(tlist)
    return (finallist)

def randomfill(sudoku, listofblocks):
    for block in listofblocks:
        for box in block:
            if sudoku[box[0],box[1]]==0:
                currentblock = sudoku[block[0][0]:(block[-1][0]+1),block[0][1]:(block[-1][1]+1)]
                sudoku[box[0],box[1]]=random.choice([i for i in range(1,10) if i not in currentblock])
    return sudoku



def TwoBoxesWithinBlock(fixed_sudoku, block):
    while(1):
        first=random.choice (block)
        second=random.choice([box for box in block if box is not first])
        
        if fixed_sudoku[first[0],first[1]] !=1 and fixed_sudoku[second[0],second[1]]!=1:
            return [first,second]
        
def flip(sudoku,toflip) :
    prosudoku=np.copy(sudoku)
    prosudoku[toflip[0][0],toflip[0][1]],prosudoku[toflip[1][0],toflip[1][1]]=prosudoku[toflip[1][0],toflip[1][1]],prosudoku[toflip[0][0],toflip[0][1]]
    return prosudoku

def sumofblock(sudoku,block) :
    s=0
    for box in block:
        s+=sudoku[box[0],box[1]]
    return s

def proposedstate(sudoku, fixedsudoku, listofblocks):
    randomblock=random.choice(listofblocks)
    if sumofblock(fixedsudoku,randomblock)>6:
        return (sudoku,1,1)
    boxestoflip = TwoBoxesWithinBlock(fixedsudoku,randomblock)
    proposedsudoku = flip(sudoku, boxestoflip)
    return [proposedsudoku,boxestoflip]

def ChooseNewState (currentSudoku, fixedSudoku, listofBlocks, sigma):
    proposal=proposedstate(currentSudoku, fixedSudoku, listofBlocks)
    newSudoku=proposal[0]
    boxestocheck =proposal[1]
    currentCost = costRowColumn(boxestocheck[0][0],boxestocheck[0][1],currentSudoku) + costRowColumn(boxestocheck[1][0],boxestocheck[1][1],currentSudoku)
    newCost = costRowColumn(boxestocheck[0][0],boxestocheck[0][1],newSudoku) + costRowColumn(boxestocheck[1][0],boxestocheck[1][1],newSudoku)
    costdif=newCost-currentCost
    rho = math.exp(-costdif/sigma)
    if (np.random.uniform(1,0,1)< rho):
        return [newSudoku, costdif]
    return [currentSudoku,0]

def noofiterations (fixedSudoku) :
    nofiter=0
    for i in range (0,9):
        for j in range (0,9):
            if fixedSudoku[i][j]!=0 :
                nofiter+=1
    return nofiter

def initialsigma (sudoku, fixedSudoku, listofBlocks):
    listdif = []
    tmpsudoku=sudoku
    for i in range(1,10) :
        tmpsudoku = proposedstate (tmpsudoku, fixedSudoku, listofBlocks)[0]
        listdif.append(cost(tmpsudoku))
    return statistics.pstdev(listdif)

def solveSudoku (sudoku) :
    sol=0
    while (sol==0) :
        decreasefac=0.99
        stuckCount=0
        fixedsudoku = np.copy(sudoku)
        PrintSudoku(sudoku)
        FixedSudokuValues(fixedsudoku)
        listblocks = createlistblocks()
        tmpsudoku = randomfill (sudoku,listblocks)
        sigma= initialsigma(sudoku,fixedsudoku,listblocks)
        score=cost(tmpsudoku)
        iter=noofiterations(fixedsudoku)
        
        if score<=0:
            sol=1
        
        while sol==0:
            prescore=score
            for i in range (0,iter):
                newstate=ChooseNewState(tmpsudoku,fixedsudoku,listblocks,sigma)
                tmpsudoku=newstate[0]
                scoredif=newstate[1]
                score+=scoredif
                print (score)
                if score<=0:
                    sol=1
                    break
            
            sigma*=decreasefac

            if score<=0:
                sol=1
                break
            if score>=prescore:
                stuckCount+=1
            else:
                stuckCount=0
            
            if stuckCount>200:
                sigma+=2
            if (cost(tmpsudoku)==0) :
                PrintSudoku(tmpsudoku)
                break

    return tmpsudoku
    
solution =solveSudoku(sdk)
print(cost(solution))
PrintSudoku(solution)
