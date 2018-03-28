# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:07:22 2018

@author: Aaron

"""
import pandas as pd
import time

def write_to_hdf(symbol,exchange_name,df):
    key = symbol+'_'+exchange_name
    path = 'orderbook/'+key+'.h5'
    store = pd.HDFStore(path)
    store.put(key,df,'t')
    time.sleep(2)
    store.close()
    pass
 
def retrieve_hdf_data(symbol,exchange_name,df):
    key = symbol+'_'+exchange_name
    path = 'orderbook/'+key+'.h5'
    store = pd.HDFStore(path)
    df = store[key]
    store.close()
    return df


def append_to_hdf(symbol,exchange_name,df):
    key = symbol+'_'+exchange_name
    path = 'orderbook/'+key+'.h5'
    store = pd.HDFStore(path)
    store.append(key,df,ignore_index=True)
    store.close()
    pass