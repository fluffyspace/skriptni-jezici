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
