#!/bin/bash
while :
do
	python3 orderbook_hdf.py
	pip install ccxt --upgrade
done
