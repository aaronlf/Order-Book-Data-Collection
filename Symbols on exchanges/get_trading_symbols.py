# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:22:40 2018

@author: Aaron
"""
# NOTE: MOST PRINT STATEMENTS HAVE BEEN COMMENTED OUT. 

import ccxt
from collections import Counter


#------------------------------------------------------------------------------


exchanges_and_symbols = {
        'acx':[],
        'anxpro':[],
        'bibox':[],
        'binance':[],
        'bitfinex':[],
        'bitlish':[],
        'bitstamp':[],
        'bittrex':[],
        'bleutrade':[], 
        'cryptopia':[], 
        'dsx':[], 
        'exmo':[], 
        'gateio':[],
        'hitbtc':[],
        'huobipro':[],
        'kraken':[],
        'kucoin':[],
        'liqui':[],
        'livecoin':[],
        'okex':[],
        'poloniex':[],
        'quadrigacx':[],
        'southxchange':[],
        'tidex':[],
        'zaif':[]
        }

#------------------------------------------------------------------------------


fiat_quotes = ['EUR','USD','CAD','GBP','RUR','PLN','AUD','BRL',
               'NZD','RUB','JPY','CHF','CNY','MXN','HKD','KRW']

#------------------------------------------------------------------------------


def main():
    initialise_and_fetch_symbols()
    delete_fiat_symbols()
    count_symbols_per_exchange()
    
    
#------------------------------------------------------------------------------


def initialise_and_fetch_symbols():
    #print("Loading markets...")
    for i in exchanges_and_symbols:
        exch = getattr(ccxt,i)()
        try:
            if i == 'bibox':
                exch.apiKey = 'acfa89fffbc601a51fed22f7c954b9320a23ec81' #PUBLIC KEY
                exch.secret = '4af367bc9e6f5b6152b2664afb01af551ca9c52d'
                exch.loadMarkets()
                exchanges_and_symbols[i] = exch.symbols
            else:
                exch.loadMarkets()
                exchanges_and_symbols[i] = exch.symbols
        except:
            print("EXCHANGE '"+str(exch.name)+"' CONNECTION FAILED")
    #print("Markets loaded.\n")
    
    
#------------------------------------------------------------------------------   
        
        
def delete_fiat_symbols():
    for i in exchanges_and_symbols:
            try:
                filtered_list = [x for x in exchanges_and_symbols[i] if x.split('/')[1] not in fiat_quotes]
                exchanges_and_symbols[i] = filtered_list
            except:
                print('Error deleting fiat symbols from '+str(i))
    remove_dead_cryptopia_pairs()


#------------------------------------------------------------------------------


def remove_dead_cryptopia_pairs():
    pairs = [i for i in exchanges_and_symbols['cryptopia'] if i.split('/')[1] not in ['DOGE','LTC']]
    exchanges_and_symbols['cryptopia'] = pairs
    
    
#------------------------------------------------------------------------------
    
    
def collect_symbols_to_list():
    #print("Putting symbols into big list...")
    big_list = []
    for i in exchanges_and_symbols:
        i_list = list(exchanges_and_symbols[i])
        for j in i_list:
            big_list.append(j)
    #print("Big list collected. \nLength =",len(big_list))
    return big_list


#------------------------------------------------------------------------------
    

def narrow_down_list():
    big_list = collect_symbols_to_list()
    #print('\nNarrowing down big list...')
    narrowed_list = []
    narrowed_dict = Counter(big_list)
    for i in narrowed_dict:
        if narrowed_dict[i] > 1:
            narrowed_list.append(i)
    #print("List has been narrowed down. \nNumber of different symbols =",len(narrowed_list))
    return narrowed_list


#------------------------------------------------------------------------------
    

def organize_symbols():
    small_list = narrow_down_list()
    new_exchange_dict = {}
    test_list = [] # Test whether or not symbols do indeed have places in more than one exchange
    
    for ex in exchanges_and_symbols:
        new_exchange_dict[ex] = [] # Empty list for the exchange in the new_exchange dictionary
        symbols = exchanges_and_symbols[ex]
        
        for i in symbols:
            if i in small_list:
                new_exchange_dict[ex].append(i)
                test_list.append(i)
    
    #print(Counter(test_list)) # This is proof that each symbol occurs more than once
    #print()
    #for j in sorted(new_exchange_dict):
        #print("'"+str(j)+"':"+str(new_exchange_dict[j])+",\n") # This is for tidy output as it will be copied and pasted into a Python file        
    #print()
    return new_exchange_dict


#------------------------------------------------------------------------------


def count_symbols_per_exchange():
    new_dict = organize_symbols()
    for exchange in sorted(new_dict):
        #print(new_dict)
        print(str(exchange)+" - Number of trading symbols: "+str(len(new_dict[exchange])))
        

#------------------------------------------------------------------------------
        
main()