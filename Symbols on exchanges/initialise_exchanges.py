# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 18:22:34 2018

@author: Aaron
"""


# INCLUDE INFO HERE:
# SERVERS 1-10 ARE BASED IN USA
# SERVERS 11-20 ARE BASED IN EUROPE
# ETC.


import get_trading_symbols


#------------------------------------------------------------------------------


exchange_servers = {
        'acx':{"servers":list(range(0,10))}, # Servers 0-9 . example. Edit this
        'anxpro':{"servers":list(range(0,10))},
        'bibox':{"servers":list(range(0,10))},
        'binance':{"servers":list(range(0,10))},
        'bitfinex':{"servers":list(range(0,10))},
        'bitlish':{"servers":list(range(0,10))},
        'bitstamp':{"servers":list(range(0,10))},
        'bittrex':{"servers":list(range(0,10))},
        'bleutrade':{"servers":list(range(0,10))}, 
        'cryptopia':{"servers":list(range(0,10))}, 
        'dsx':{"servers":list(range(0,10))}, 
        'exmo':{"servers":list(range(0,10))}, 
        'gateio':{"servers":list(range(0,10))},
        'hitbtc':{"servers":list(range(0,10))},
        'huobipro':{"servers":list(range(0,10))},
        'kraken':{"servers":list(range(0,6))},
        'kucoin':{"servers":list(range(0,10))},
        'liqui':{"servers":list(range(0,10))},
        'livecoin':{"servers":list(range(0,10))},
        'okex':{"servers":list(range(0,10))},
        'poloniex':{"servers":list(range(0,10))},
        'quadrigacx':{"servers":list(range(0,10))},
        'southxchange':{"servers":list(range(0,10))},
        'tidex':{"servers":list(range(0,10))},
        'zaif':{"servers":list(range(0,10))}
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
                exchange_servers[i]['symbols'] = exchanges_and_symbols[i]['symbols']
                exchange_servers[i]['exch_object'] = exchanges_and_symbols[i]['exch_object']

#------------------------------------------------------------------------------
                
                
def designate(server_num):
    for i in exchange_servers:
        servers = exchange_servers[i]['servers']
        
        if server_num in servers:
            symbols = exchange_servers[i]['symbols']
            
            amount_of_symbols = len(symbols)
            amount_of_servers = len(servers)
        
            in_each = amount_of_symbols // amount_of_servers
            remainder = amount_of_symbols % amount_of_servers
            
            index = servers.index(server_num)
            symbols_needed = symbols[in_each*index:in_each*(index+1)]
            if index < remainder:
                symbols_needed.append(symbols[(amount_of_servers*in_each)+index])
            exchange_servers[i]['symbols'] = symbols_needed
        else:
            exchange_servers[i]['symbols'] = []
    return exchange_servers
            

#------------------------------------------------------------------------------
            
            
def main(n):
    add_symbols_to_dict()
    return designate(n)


#------------------------------------------------------------------------------
    
serverNumber = 1
exchanges = main(serverNumber)

#------------------------------------------------------------------------------