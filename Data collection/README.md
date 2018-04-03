### Setting up working directory
##### 1) Copy the following files to the working directory (Unix/Linux)
- *orderbook_collect.sh*
- *orderbook_hdf.py*
- *setup.sh*  
- *get_symbols.py*
- *initialise_exchanges.py*

##### 2) Get the necessary dependencies
`$ bash setup.sh`  

##### 3) Create an empty folder called 'orderbook' in the working directory
This is where h5 files will be saved to.

### How to run file
`$ bash orderbook_collect.sh`

Note: If bash scripts are not working, you may need to perform an EOL conversion from Windows to Linux. This can be done through *Notepad++* under the Edit tab. This problem shouldn't crop up, however.