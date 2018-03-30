# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:07:22 2018
@author: Aaron
"""
import pandas as pd
import time
import numpy as np
import sched
import threading
import initialise_exchanges


#------------------------------------------------------------------------------


def write_to_hdf(symbol,exchange_name,df):
    symbol = '_'.join(symbol.split('/'))
    key = symbol+'_'+exchange_name
    path = 'orderbook/'+key+'.h5'
    store = pd.HDFStore(path)
    store.put(key,df,'t')
    time.sleep(2)
    store.close()
    pass
 
    
def retrieve_hdf_data(symbol,exchange_name):
    symbol = '_'.join(symbol.split('/'))
    key = symbol+'_'+exchange_name
    path = 'orderbook/'+key+'.h5'
    store = pd.HDFStore(path)
    df = store[key]
    store.close()
    return df


def append_to_hdf(symbol,exchange_name,df):
    symbol = '_'.join(symbol.split('/'))
    key = symbol+'_'+exchange_name
    path = 'orderbook/'+key+'.h5'
    store = pd.HDFStore(path)
    store.append(key,df,ignore_index=True)
    store.close()
    pass


#------------------------------------------------------------------------------
    

def get_orderbook(symbol,exch_object):
    orderbook = fetch_orders_safely(symbol,exch_object)
    precision = exch_object.markets[symbol]['precision']
    timestamp = orderbook['timestamp']    
    bid_volume = 0
    bid_weighted_price = 0
    bids = orderbook['bids'][:3]
    for i in bids:
        bid_volume += i[1]
        bid_weighted_price += i[0]*i[1]
    bid_weighted_price = bid_weighted_price / bid_volume
    bid_volume = 0
    for i in bids:
        if i[0] >= bid_weighted_price:
            bid_volume += i[1]
    ask_volume = 0
    ask_weighted_price = 0
    asks = orderbook['asks'][:3]
    for i in asks:
        ask_volume += i[1]
        ask_weighted_price += i[0]*i[1]
    ask_weighted_price = ask_weighted_price / ask_volume
    ask_volume = 0
    for i in asks:
        if i[0] <= ask_weighted_price:
            ask_volume += i[1]
    orderbook_dict = {
            'timestamp':[timestamp],
            'bid_price':[round(bid_weighted_price,precision['price'])],
            'bid_volume':[round(bid_volume,precision['amount'])],
            'ask_price':[round(ask_weighted_price,precision['price'])],
            'ask_volume':[round(ask_volume,precision['amount'])]}
    df = pd.DataFrame(orderbook_dict)
    orderbook_df = convert_orderbook_dtypes(df,precision)
    return orderbook_df
    

def fetch_orders_safely(sym,obj):
    try:
        orderbook = obj.fetch_l2_order_book(sym,3)
    except:
        print("Note: There was an error fetching the "+sym+" orderbook for "+obj.name)
        time.sleep(3)
        orderbook = fetch_orders_safely(obj,sym)
    return orderbook
    
    
def convert_orderbook_dtypes(df,precision):
    if precision['price'] < 7:
        price_dtype = np.float32
    else:
        price_dtype = np.float64
    if precision['amount'] < 7:
        volume_dtype = np.float32
    else:
        volume_dtype = np.float64
    new_df = df.astype({
            'bid_price':price_dtype,
            'bid_volume':volume_dtype,
            'ask_price':price_dtype,
            'ask_volume':volume_dtype})
    return new_df
    
    
#------------------------------------------------------------------------------    

    
def collect_data(symbol,exch_object):
    exchange_name = exch_object.name
    orderbook = get_orderbook(symbol,exch_object)
    try:
        retrieve_hdf_data(symbol,exchange_name)
    except KeyError:
        write_to_hdf(symbol,exchange_name,orderbook)
    else:
        append_to_hdf(symbol,exchange_name,orderbook)
    with threading.Lock():
        print("Collected data for "+symbol+" on "+exchange_name)

def scheduled_task(exchange):
    exch_object = exchange['exch_object']
    all_symbols = exchange['symbols']
    rateLimit = exch_object.rateLimit / 1000
    s = sched.scheduler()
    while len(all_symbols) > 0:
        for symbol in all_symbols:
            s.enter(rateLimit,0,collect_data,argument=(symbol,exch_object))
            s.run()
    pass


#------------------------------------------------------------------------------
    

def set_threads(exchanges):
    threads_of_exchanges = []
    for exchange in exchanges:
        threads_of_exchanges.append(threading.Thread(target=scheduled_task,kwargs={'exchange':exchange},daemon=True))
    for i in threads_of_exchanges:
        i.start()
    for i in threads_of_exchanges:
        i.join()
        
        
#------------------------------------------------------------------------------ 


exchanges = initialise_exchanges.exchanges
if __name__ == '__main__':
    set_threads(exchanges)     
        