from Tkinter import *

def logModification(var,*args):
    print 'variable '+var+' has been modified'

window=Tk()

b1=Button(window,text='WHATSUPPPP',command=lambda : t1.insert(END,e1_value.get()*6))
b1.grid(row=0,column=0)
e1_value=StringVar()
obsv1=e1_value.trace('w',logModification)
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1)
t1=Text(window,height=1,width=20)
t1.grid(row=0,column=2)

window.mainloop()