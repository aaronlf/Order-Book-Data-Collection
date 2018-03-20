# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 23:34:03 2018

@author: Aaron
"""

import pairs_on_exchanges
from collections import Counter


#------------------------------------------------------------------------------


all_symbols = pairs_on_exchanges.pairs
all_exchanges = sorted(list(pairs_on_exchanges.pairs.keys()))


#------------------------------------------------------------------------------
    
    
def collect_symbols_to_list():
    print("Putting symbols into big list...")
    big_list = []
    for i in all_symbols:
        i_list = list(all_symbols[i])
        for j in i_list:
            big_list.append(j)
    print("Big list collected. \nLength =",len(big_list))
    return big_list


#------------------------------------------------------------------------------
    

def narrow_down_list():
    big_list = collect_symbols_to_list()
    print('\nNarrowing down big list...')
    narrowed_list = []
    narrowed_dict = Counter(big_list)
    for i in narrowed_dict:
        if narrowed_dict[i] > 1:
            narrowed_list.append(i)
    print("List has been narrowed down. \nNumber of different symbols =",len(narrowed_list))
    return narrowed_list


#------------------------------------------------------------------------------
    

def organize_symbols():
    small_list = narrow_down_list()
    new_exchange_dict = {}
    test_list = [] # Test whether or not symbols do indeed have places in more than one exchange
    
    for ex in all_exchanges:
        new_exchange_dict[ex] = [] # Empty list for the exchange in the new_exchange dictionary
        symbols = all_symbols[ex]
        
        for i in symbols:
            if i in small_list:
                new_exchange_dict[ex].append(i)
                test_list.append(i)
    
    print(Counter(test_list)) # This is proof that each symbol occurs more than once
    print()
    for j in sorted(new_exchange_dict):
        print("'"+str(j)+"':"+str(new_exchange_dict[j])+",\n") # This is for tidy output as it will be copied and pasted into a Python file        
    # The final comma must be skipped manually when copying and pasting
    print()
    return new_exchange_dict


#------------------------------------------------------------------------------


def count_symbols_per_exchange():
    new_dict = organize_symbols()
    for exchange in sorted(new_dict):
        #print(new_dict)
        print(str(exchange)+" - Number of trading symbols: "+str(len(new_dict[exchange])))
        

#------------------------------------------------------------------------------
        
        
count_symbols_per_exchange()