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

# za pretraživanje eurostat baze podataka po ključnom pojmu npr. 'gbard':
#   toc_df = eurostat.get_toc_df()
#   f = eurostat.subset_toc_df(toc_df, 'gbard')

# data caching
if is_non_zero_file("data"):
    with open("data", "rb") as f:
        data = pickle.load(f)
        print("Loading cached data")
else:
    data = eurostat.get_data_df('gba_nabsfin07')
    with open("data", "wb") as f:
        pickle.dump(data, f)
        print("Writing data to cache")
    
selected = []
selected_countries = [] 
prve_kategorije = []
druge_kategorije = []
trece_kategorije = []
thirddialog = None
drzave_kriterij = []

"""

NABS01 Istraživanje i eksploatacija zemlje
NABS02 Okoliš
NABS03 Istraživanje i iskorištavanje svemira
NABS04 Promet, telekomunikacije i ostala infrastr...
NABS05 Energija
NABS06 Industrijska proizvodnja i tehnologija
NABS07 Zdravlje
NABS08 Poljoprivreda
NABS09 Obrazovanje
NABS10 Kultura, rekreacija, religija i masovni mediji
NABS11 Politički i društveni sustavi, strukture i procesi
NABS12 Opće unapređenje znanja: istraživanje i razvoj financiran iz općih sveučilišnih fondova (GUF)
NABS121 Istraživanje i razvoj u vezi s prirodnim znanostima - financiran iz GUF-a
NABS122 Istraživanje i razvoj u vezi s inženjerskim znanostima - financira GUF
NABS123 Istraživanje i razvoj u vezi s medicinskim znanostima - financiran iz GUF-a
NABS124 Istraživanje i razvoj u vezi s poljoprivrednim znanostima - financiran iz GUF-a
NABS125 Istraživanje i razvoj u vezi s društvenim znanostima - financiran iz GUF-a
NABS126 Istraživanje i razvoj u vezi s humanističkim znanostima - financiran iz GUF-a
NABS13 Općenito unapređenje znanja: istraživanje i razvoj financiran iz drugih izvora osim GUF-a
NABS131 Istraživanje i razvoj u vezi s prirodnim znanostima - financirano iz drugih izvora osim GUF-a
NABS132 Istraživanje i razvoj u vezi s inženjerskim znanostima - financirano iz drugih izvora osim GUF-a
NABS133 Istraživanje i razvoj u vezi s medicinskim znanostima - financirano iz drugih izvora osim GUF-a
NABS134 Istraživanje i razvoj u vezi s poljoprivrednim znanostima - financirano iz drugih izvora osim GUF-a
NABS135 Istraživanje i razvoj u vezi s društvenim znanostima - financirano iz drugih izvora osim GUF-a
NABS136 Istraživanje i razvoj u vezi s humanističkim znanostima - financirano iz drugih izvora osim GUF-a
NABS14 Obrana
TOTAL Ukupna izdvajanja iz državnog proračuna za istraživanje i razvoj 

"""

nabs07_renamed = {
    "NABS01":"a",
    "NABS02":"b",
    "NABS03":"c",
    "NABS04":"d",
    "NABS05":"",
    "NABS06":"",
    "NABS07":"",
    "NABS08":"",
    "NABS09":"",
    "NABS10":"",
    "NABS11":"",
    "NABS12":"",
    "NABS121":"",
    "NABS122":"",
    "NABS123":"",
    "NABS124":"",
    "NABS125":"",
    "NABS126":"",
    "NABS13":"",
    "NABS131":"",
    "NABS132":"",
    "NABS133":"",
    "NABS134":"",
    "NABS135":"",
    "NABS136":"",
    "NABS14":"",
    "TOTAL":"",
    }

units_renamed = {
    "MIO_NAC": "Nacionalna valuta",
    "MIO_EUR": "Euro",
    "EUR_HAB": "Euro po stanovniku",
    "MIO_PPS": "Standard kupovne moći",
    "MIO_PPS_KP05": "Standard kupovne moći u cijenama iz 2005.",
    "PPS_HAB_KP05": "Standard kupovne moći po stanovniku na stalne cijene iz 2005.",
    "PC_GDP": "Postotak bruto domaćeg proizvoda",
    "PC_GBA": "Postotak ukupnog GBARD-a - za raščlambe po društveno-ekonomskim ciljevima i načinu financiranja",
    "PC_TOT": "Postotak ukupnog transnacionalno koordiniranog istraživanja i razvoja (za raščlambu prema kategoriji)",
    "PC_GEXP": "Postotak državnih rashoda",
    
    }

razlicite_nabs07 = data.drop_duplicates(subset = ["nabs07"])
for prva_kategorija in razlicite_nabs07['nabs07']:
    if prva_kategorija in nabs07_renamed.keys():
        prve_kategorije.append(nabs07_renamed[prva_kategorija])
    else:
        prve_kategorije.append(prva_kategorija)
    

    
def plotit():
    range_svih_godina = range(2004,2021)
    drzave = {}
    
    if len(selected) == 2:
        for godina in range_svih_godina:
            for index, row in data.loc[ \
                    (data['nabs07'] == prve_kategorije[selected[0]]) & \
                    (data['unit'] == druge_kategorije[selected[1]]) & \
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
            #print("država", drzava, ":")
            godine2 = []
            podaci = []
            for godine in drzave[drzava]:
                for godina in godine.keys():
                    godine2.append(godina)
                    podaci.append(godine[godina])
                    #print("\t", godina, "-", godine[godina])
            plotters.append(Plotter(godine2, podaci, drzava))
        TkinterFigure.draw(prve_kategorije[selected[0]] + " -> " + druge_kategorije[selected[1]], plotters)


def callback1(index, root):
    print("Ovo je callback1, prenesen je indeks " + str(index))
    selected.append(int(str(index)))
    root.destroy()
    showSecondDialog()
    
def callback2(index, root):
    print("Ovo je callback2, prenesen je indeks " + str(index))
    selected.append(int(str(index)))
    root.destroy()
    showThirdDialog()

def callback3(index, root):
    print("Ovo je callback3, prenesen je indeks " + str(index))
    if index in selected_countries:
        selected_countries.remove(index)
    else:
        selected_countries.append(index)
    #root.destroy()
    
def callbackNext(root, checkboxes, plot):
    global drzave_kriterij
    for chec in checkboxes:
        print("ukljucujem drzavu: " + trece_kategorije[chec])
        drzave_kriterij.append(trece_kategorije[chec])
    #print(checkboxes)
    root.destroy()
    if plot:
        plotit()
    else:
        print("ovdje sljedi prikazivanje podataka u konzoli za te države: TODO")
    
def showFirstDialog():
    firstdialog = TkinterRadiobuttons(callback1, 'GBARD prema socioekonomskim ciljevima')
    firstdialog.loadRadiobuttons(prve_kategorije )
    
def showSecondDialog():
    razlicite_unit = data.drop_duplicates(subset = ["unit"])
    for druga_kategorija in razlicite_unit['unit']:
        if druga_kategorija in units_renamed.keys():
            druge_kategorije.append(units_renamed[druga_kategorija])
        else:
            druge_kategorije.append(druga_kategorija)
        #druge_kategorije.append(druga_kategorija)
    
    seconddialog = TkinterRadiobuttons(callback2, 'Odaberite mjeru')
    seconddialog.loadRadiobuttons(druge_kategorije)
    #print(selected)
    
def showThirdDialog():
    global thirddialog, trece_kategorije
    
    for index, treca_kategorija in data.loc[ \
            (data['nabs07'] == prve_kategorije[selected[0]]) & \
            (data['unit'] == druge_kategorije[selected[1]]) \
            ].drop_duplicates(subset = ["geo\\time"]).iterrows():
        trece_kategorije.append(str(treca_kategorija['geo\\time']))
    print(trece_kategorije)
    thirddialog = TkinterCheckboxes(callback3, callbackNext)
    thirddialog.loadCheckboxes(trece_kategorije)
    #print(selected)
    
showFirstDialog()
#print(razlicite_nabs07['nabs07'])



#razlicite_drzave = data.drop_duplicates(subset = ["geo\\time"])

# provjerava bazu gdje nabs07 == nabs01 i gdje je unit == eur_hab
# data[(data['nabs07'] == 'NABS01') & (data['unit'] == 'EUR_HAB')]

