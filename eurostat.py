# -*- coding: utf-8 -*-
"""
Created on Sun Jan 16 13:21:48 2022

@author: Ingo Kodba & Stjepan Rus

tutorials:
https://pypi.org/project/eurostat/
https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Tutorial:Symbols_and_abbreviations

database:
https://ec.europa.eu/eurostat/data/database

"""

import eurostat
import pickle
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

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
print(razlicite_nabs07['nabs07'])

# provjerava bazu gdje nabs07 == nabs01 i gdje je unit == eur_hab
# data[(data['nabs07'] == 'NABS01') & (data['unit'] == 'EUR_HAB')]

godine = range(2004,2021)
drzave = {}
nabs07_kriterij = 'NABS01'
unit_kriterij = 'EUR_HAB'
drzave_kriterij = ['HR', 'SI', 'DE', 'FR', 'UK']

for godina in godine:
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
       
plt.figure()

       
for drzava in drzave:
    print("država", drzava, ":")
    godine2 = []
    podaci = []
    for godina in drzave[drzava]:
        for kljuc in godina.keys():
            godine2.append(kljuc)
            podaci.append(godina[kljuc])
            print("\t", kljuc, "-", godina[kljuc])
    plt.plot(godine2, podaci, 'o-', linewidth=1, markersize=3, label=drzava);  # Plot some data on the axes.
plt.legend()
plt.title('NABS01: EUR_HAB')
plt.show()

