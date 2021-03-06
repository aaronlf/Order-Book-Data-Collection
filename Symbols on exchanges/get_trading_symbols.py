# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 11:22:40 2018

@author: Aaron
"""
# NOTE: MOST PRINT STATEMENTS HAVE BEEN COMMENTED OUT. 

import ccxt
from collections import Counter
import time


#------------------------------------------------------------------------------


exchanges_and_symbols = {
        'acx':{},
        'anxpro':{},
        'bibox':{},
        'binance':{},
        'bitfinex':{},
        'bitlish':{},
        'bitstamp':{},
        'bittrex':{},
        'bleutrade':{}, 
        'dsx':{}, 
        'exmo':{}, 
        'gateio':{},
        'huobipro':{},
        'kraken':{},
        'kucoin':{},
        'liqui':{},
        'livecoin':{},
        'okex':{},
        'poloniex':{},
        'quadrigacx':{},
        'southxchange':{},
        'tidex':{},
        'zaif':{}
        }

#------------------------------------------------------------------------------


fiat_quotes = ['EUR','USD','CAD','GBP','RUR','PLN','AUD','BRL',
               'NZD','RUB','JPY','CHF','CNY','MXN','HKD','KRW']

#------------------------------------------------------------------------------


def main():
    initialise_and_fetch_symbols()
    delete_fiat_symbols()
    print()
    return count_symbols_per_exchange()
    

#------------------------------------------------------------------------------


def initialise_and_fetch_symbols():
    #print("Loading markets...")
    for exchange in exchanges_and_symbols:
        exch = fetch(exchange)
        if exch == False:
            print("\nEXCHANGE '"+str(exchange)+"' CONNECTION FAILED. TRYING AGAIN...\n")
            time.sleep(10)
            if fetch(exchange) == False:
                exchanges_and_symbols[exchange]['symbols'] = []
        exchanges_and_symbols[exchange]['exch_object'] = exch
    #print("Markets loaded.\n")
    
    
#------------------------------------------------------------------------------
    
    
def fetch(exchange):
    exch = getattr(ccxt,exchange)()
    try:
        if exchange == 'bibox':
            exch.apiKey = 'acfa89fffbc601a51fed22f7c954b9320a23ec81' #PUBLIC KEY
            exch.secret = '4af367bc9e6f5b6152b2664afb01af551ca9c52d'
            exch.loadMarkets()
            exchanges_and_symbols[exchange]['symbols'] = exch.symbols
        else:
            exch.loadMarkets()
            exchanges_and_symbols[exchange]['symbols'] = exch.symbols
    except:
        return False
    else:
        return exch
            
            
#------------------------------------------------------------------------------       


def delete_fiat_symbols():
    #remove_dead_cryptopia_pairs()
    remove_bad_kraken_pairs()
    for i in exchanges_and_symbols:
        try:
            filtered_list = [x for x in exchanges_and_symbols[i]['symbols'] if x.split('/')[1] not in fiat_quotes]
            exchanges_and_symbols[i]['symbols'] = filtered_list
        except:
            print('Error deleting fiat symbols from '+str(i))


#------------------------------------------------------------------------------

'''
def remove_dead_cryptopia_pairs():
    pairs = [i for i in exchanges_and_symbols['cryptopia']['symbols'] if i.split('/')[1] not in ['DOGE']]
    exchanges_and_symbols['cryptopia']['symbols'] = pairs
'''    
    
#------------------------------------------------------------------------------


def remove_bad_kraken_pairs():
    bad_pairs = ['ETHCAD.d', 'ETHEUR.d', 'ETHGBP.d', 'ETHJPY.d', 
                 'ETHUSD.d', 'ETHXBT.d','XBTCAD.d', 'XBTEUR.d', 
                 'XBTGBP.d', 'XBTJPY.d', 'XBTUSD.d']
    pairs = [i for i in exchanges_and_symbols['kraken']['symbols'] if i not in bad_pairs]
    exchanges_and_symbols['kraken']['symbols'] = pairs
    
    
#------------------------------------------------------------------------------
    
    
def collect_symbols_to_list():
    #print("Putting symbols into big list...")
    big_list = []
    for i in exchanges_and_symbols:
        i_list = list(exchanges_and_symbols[i]['symbols'])
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
        new_exchange_dict[ex] = {} # Empty dict for the exchange in the new_exchange dictionary
        symbols = exchanges_and_symbols[ex]['symbols']
        new_exchange_dict[ex]['exch_object'] = exchanges_and_symbols[ex]['exch_object']
        new_exchange_dict[ex]['symbols'] = []
        
        for i in symbols:
            if i in small_list:
                new_exchange_dict[ex]['symbols'].append(i)
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
    total_symbols = 0
    for exchange in sorted(new_dict):
        num_of_symbols = len(new_dict[exchange]['symbols'])
        total_symbols += num_of_symbols
        print(str(exchange)+" - Number of trading symbols: "+str(num_of_symbols))
    print("\nTotal number of symbols:",total_symbols,'\n')
    return new_dict


#------------------------------------------------------------------------------