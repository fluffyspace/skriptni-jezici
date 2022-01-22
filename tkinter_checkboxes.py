# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 12:14:22 2022

@author: Krepana Krava
"""

from tkinter import *

class TkinterCheckboxes:
    
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
    
    def sel():
        selection = "You selected the option " + str(var.get())
        label.config(text = selection)

    
    #def passChosenToCallback():
        
        
    def loadCheckboxes(labels):
        master = Tk()
        var1 = IntVar()
        counter = 0
        for label in labels:
            Checkbutton(master, text=label, variable=counter).grid(row=counter, sticky=W)
            counter += 1
        label = Label(master)
        label.pack()
        Button(master, text='Quit', command=master.destroy).grid(row=0, column=1, sticky=E, pady=4)
        Button(master, text='Show', command=master.destroy).grid(row=1, column=1, sticky=E, pady=4)
        mainloop()
        
TkinterCheckboxes.loadCheckboxes(["bmw", "audi", "mercedes", "folksvagen"])