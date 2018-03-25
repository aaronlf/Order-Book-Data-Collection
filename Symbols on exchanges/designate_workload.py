# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:22:34 2018

@author: Aaron
"""


'''

NEEDS TO ACCEPT A DITIONARY OF ALL THE EXCHANGES AND SYMBOLS THAT HAVE BEEN LOADED.

THERE SHOULD ALSO BE VALUES IN THE DICTIONARY ASSINGING CERTAIN EXCHANGES WITH 
CERTAIN SERVERS.

THE FUNCTION USED IN THIS SCRIPT SHOULD TAKE THE SERVER NUMBER AS AN ARGUMENT.
THIS SERVER NUMBER WILL BE ASSIGNED TO THE MAIN DATA COLLECTION PROGRAM INDIVIDUALLY, 
DEPENDING ON WHAT SERVER IT WILL BE RUN FROM.

IMPORTANT NOTE: CAN **NOT** HAVE TWO DIFFERENT SERVERS WRITING TO THE SAME H5 FILE
AS EACH SERVER WILL ACTUALLY HAVE ITS OWN SEPARATE COPY

'''
# INCLUDE INFO HERE:
# SERVERS 1-10 ARE BASED IN USA
# SERVERS 11-20 ARE BASED IN EUROPE
# ETC.


import get_trading_symbols


#------------------------------------------------------------------------------


exchange_servers = {
        'acx':{"servers":list(range(1,11))}, # Servers 1-10 . example. Edit this
        'anxpro':{"servers":list(range(1,11))},
        'bibox':{"servers":list(range(1,11))},
        'binance':{"servers":list(range(1,11))},
        'bitfinex':{"servers":list(range(1,11))},
        'bitlish':{"servers":list(range(1,11))},
        'bitstamp':{"servers":list(range(1,11))},
        'bittrex':{"servers":list(range(1,11))},
        'bleutrade':{"servers":list(range(1,11))}, 
        'cryptopia':{"servers":list(range(1,11))}, 
        'dsx':{"servers":list(range(1,11))}, 
        'exmo':{"servers":list(range(1,11))}, 
        'gateio':{"servers":list(range(1,11))},
        'hitbtc':{"servers":list(range(1,11))},
        'huobipro':{"servers":list(range(1,11))},
        'kraken':{"servers":list(range(1,11))},
        'kucoin':{"servers":list(range(1,11))},
        'liqui':{"servers":list(range(1,11))},
        'livecoin':{"servers":list(range(1,11))},
        'okex':{"servers":list(range(1,11))},
        'poloniex':{"servers":list(range(1,11))},
        'quadrigacx':{"servers":list(range(1,11))},
        'southxchange':{"servers":list(range(1,11))},
        'tidex':{"servers":list(range(1,11))},
        'zaif':{"servers":list(range(1,11))}
        }


#------------------------------------------------------------------------------


def add_symbols_to_dict():
    '''
    This function takes the dictionary from the "get_trading_symbols" script 
    and combines it with the dictionary defined above. In future, these two 
    scripts might just be combined into one, named "initialise.py"
    '''
    exchanges_and_symbols = get_trading_symbols.main()
    for i in exchanges_and_symbols:
        for j in exchange_servers:
            if i == j:
                exchange_servers[i]['symbols'] = exchange_and_symbols[i]['symbols']
                exchange_servers[i]['exch_object'] = exchange_and_symbols[i]['exch_object']

#------------------------------------------------------------------------------
                
                
def 
