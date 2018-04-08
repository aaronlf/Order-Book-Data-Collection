#!/bin/bash
while :
do
 pip3 install ccxt --upgrade
 python3 orderbook_hdf.py 0
done 
