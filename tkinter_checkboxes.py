# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 12:14:22 2022

@author: Krepana Krava
"""

from tkinter import *

class TkinterCheckboxes:
    
    def __init__(self, selected_callback, next_callback):
        self.root = Tk()
        self.root.wm_title('Odaberite države')
        self.label = Label(self.root)
        self.selected_callback = selected_callback
        self.next_callback = next_callback
        self.vars = []
    
    def sel(self):
        index_selected = self.var.get()
        selection = "You selected the option " + str(index_selected)
        self.label.config(text = selection)
        self.selected_callback(index_selected, self.root)
        
    def getAllChecked(self):
        counter = 0
        checked = []
        for var in self.vars:
            #print(var.get())
            if var.get() == 1:
                checked.append(counter)
            counter += 1
        return checked
    
    def drawCountries(self):
        self.next_callback(self.root, self.getAllChecked(), True)
        
    def printCountries(self):
        self.next_callback(self.root, self.getAllChecked(), False)
    
    def loadCheckboxes(self, labels):
        counter = 0
        button = Button(master=self.root, text="Prikaži graf", command=self.drawCountries)
        button.pack()
        button = Button(master=self.root, text="Ispiši podatke", command=self.printCountries)
        button.pack()
        
        leftframe = Frame(self.root)
        leftframe.pack( side = LEFT )
        rightframe = Frame(self.root)
        rightframe.pack( side = RIGHT )
        
        for labela in labels:
            var = IntVar()
            if counter < 20:
                R1 = Checkbutton(leftframe, text=labela, variable=var, onvalue=1, offvalue=0)
            else:
                R1 = Checkbutton(rightframe, text=labela, variable=var, onvalue=1, offvalue=0)
            
            self.vars.append(var)
            R1.pack( anchor = W )
            counter += 1
        self.label.pack()
        self.root.geometry("500x800")
        self.root.mainloop()
