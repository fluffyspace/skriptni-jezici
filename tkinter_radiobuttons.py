# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 20:09:40 2022

@author: Krepana Krava
"""

from tkinter import *

class TkinterRadiobuttons:
    
    def __init__(self, callback, title):
        self.root = Tk()
        self.root.wm_title(title)
        self.label = Label(self.root)
        self.callback = callback
        self.var = IntVar()
    
    def sel(self):
        index_selected = self.var.get()
        selection = "You selected the option " + str(index_selected)
        self.label.config(text = selection)
        self.callback(index_selected, self.root)
    
    def loadRadiobuttons(self, labels):
        counter = 0
        for labela in labels:
            R1 = Radiobutton(self.root, text=labela, variable=self.var, value=counter, command=self.sel)
            R1.pack( anchor = W )
            counter += 1
        
        self.label.pack()
        self.root.geometry("750x700")
        self.root.mainloop()
