# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 13:21:48 2022

@author: Ingo Kodba & Stjepan Rus

Mora se instalirati eurostat modul s "pip install eurostat". Nakon toga u spyderu (bar meni tako) u konzolu upisati i pokrenuti "import eurostat", i tek onda pokrenuti program. Inače mi izbaci neki eurostat error.

Tutorials:
https://pypi.org/project/eurostat/
https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Tutorial:Symbols_and_abbreviations

Database:
https://ec.europa.eu/eurostat/data/database
"""

import eurostat
import pickle
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from tkinter_figure import Plotter
from tkinter_figure import TkinterFigure
from tkinter_checkboxes import TkinterCheckboxes
from tkinter_radiobuttons import TkinterRadiobuttons

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

# pretraživanje eurostat baze podataka po ključnom pojmu npr. 'gbard'
#toc_df = eurostat.get_toc_df()
#f = eurostat.subset_toc_df(toc_df, 'gbard')

if is_non_zero_file("data"):
    with open("data", "rb") as f:
        data = pickle.load(f)
        print("Loading cached data")
else:
    data = eurostat.get_data_df('gba_nabsfin07')
    with open("data", "wb") as f:
        pickle.dump(data, f)
        print("Writing data to cache")
        
razlicite_nabs07 = data.drop_duplicates(subset = ["nabs07"])
prve_kategorije = []
for prva_kategorija in razlicite_nabs07['nabs07']:
    prve_kategorije.append(prva_kategorija)
    
    
def showNextDialog(index, root):
    print("ovdje ponuditi drugi meni, odnosno nakon obdabira nabs07 kategorije, ponuditi unit kategoriju")
    print("Ovo je callback, prenesen je indeks " + str(index))
    root.destroy()
    
firstdialog = TkinterRadiobuttons(showNextDialog)
firstdialog.loadRadiobuttons(prve_kategorije )
print(razlicite_nabs07['nabs07'])

# provjerava bazu gdje nabs07 == nabs01 i gdje je unit == eur_hab
# data[(data['nabs07'] == 'NABS01') & (data['unit'] == 'EUR_HAB')]

range_svih_godina = range(2004,2021)
drzave = {}
nabs07_kriterij = 'NABS01'
unit_kriterij = 'EUR_HAB'
drzave_kriterij = ['HR', 'SI', 'DE', 'FR', 'UK']

for godina in range_svih_godina:
    for index, row in data.loc[ \
            (data['nabs07'] == nabs07_kriterij) & \
            (data['unit'] == unit_kriterij) & \
            (data[godina]) & \
            (data['geo\\time'].isin(drzave_kriterij)) \
            ].iterrows():
        drzava = row['geo\\time']
        if drzava not in drzave:
            drzave[drzava] = [{godina:row[godina]}]
        else:
            drzave[drzava].append({godina:row[godina]})
        #print(row['geo\\time'], godina, row[godina])

plotters = []       
for drzava in drzave:
    print("država", drzava, ":")
    godine2 = []
    podaci = []
    for godine in drzave[drzava]:
        for godina in godine.keys():
            godine2.append(godina)
            podaci.append(godine[godina])
            print("\t", godina, "-", godine[godina])
    plotters.append(Plotter(godine2, podaci, drzava))
TkinterFigure.draw(plotters)
