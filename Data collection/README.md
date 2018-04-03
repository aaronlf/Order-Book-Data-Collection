### Setting up working directory
##### 1) Move the following files to the working directory:
- *get_symbols.py*  
- *initialise_exchanges.py*  
- *orderbook_hdf.py*  
- *setup.sh*
- *orderbook_collect.sh*

##### 2) Get the necessary dependencies:
`bash setup.sh`  

##### 3) Create an empty folder called 'orderbook' in the working directory
This is where h5 files will be saved to.

### How to run file
`bash orderbook_collect.sh`

Note: If bash scripts are not working, you may need to perform an EOL conversion from Windows to Linux. This can be done through Notepad++ under the Edit tab. This problem shouldn't crop up, however.
