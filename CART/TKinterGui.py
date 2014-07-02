# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 09:59:21 2014

@author: uncle_bai
"""

import CART
from numpy import *
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def reDraw(tolS,tolN):
    reDraw.f.clf()
    reDraw.a=reDraw.f.add_subplot(111)
    if chkBtnVar.get():
        if tolN<2:
            tolN=2
        data=reDraw.rawDat
        data=hstack(((mat(ones((data.shape[0],1)))),data))    
        mytree=CART.creatTree(data,CART.modelLeaf,CART.modelErr,(tolS,tolN))
        testdata=hstack(((mat(ones((reDraw.testDat.shape[0],1)))),reDraw.testDat))    
        yHat=CART.predict(mytree,testdata,CART.modelTreeEval)
    else:
        mytree=CART.creatTree(reDraw.rawDat,CART.regLeaf,CART.regErr,(tolS,tolN))
        yHat=CART.predict(mytree,reDraw.testDat,CART.regTreeEval)
    reDraw.a.scatter(array(reDraw.rawDat[:,0]),array(reDraw.rawDat[:,1]),s=5)
    reDraw.a.plot(reDraw.testDat,yHat,linewidth=2.0)
    reDraw.canvas.show()

def getinput():
    try:
        tolN=int(tolNentry.get())
        tolS=float(tolSentry.get())
    except:
        print 'false parameter'
        tolN=4
        tolS=1.0
    return tolN,tolS
        
def drawNewTree():
    tolN,tolS=getinput()
    reDraw(tolS,tolN)
    
root=Tk()
Label(root,text='plot place hold').grid(row=0,columnspan=3)
Label(root,text='tolN').grid(row=1,column=0)
tolNentry=Entry(root)
tolNentry.grid(row=1,column=1)
tolNentry.insert(0,'10')
Label(root,text='tolS').grid(row=2,column=0)
tolSentry=Entry(root)
tolSentry.grid(row=2,column=1)
tolSentry.insert(0,'1.0')
Button(root,text='Redraw',command=drawNewTree).grid(row=1,column=2,rowspan=2)
chkBtnVar=IntVar()
chkBtn=Checkbutton(root,text='Model Tree',variable=chkBtnVar)
chkBtn.grid(row=3,column=0,columnspan=2)

reDraw.rawDat=mat(CART.file2data('sine.txt'))
reDraw.testDat=mat(arange(min(reDraw.rawDat[:,0]),max(reDraw.rawDat[:,0]),0.01)).T
reDraw.f=Figure(figsize=(5,4),dpi=100)
reDraw.canvas=FigureCanvasTkAgg(reDraw.f,master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3)



reDraw(1.0,10)
root.mainloop()



