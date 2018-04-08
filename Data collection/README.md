### Setting up working directory
#### 1) Copy the following files to the working directory (Unix/Linux)
- *orderbook_collect.sh*
- *orderbook_hdf.py*
- *setup.sh*  
- *get_symbols.py*
- *initialise_exchanges.py*

#### 2) Get the necessary dependencies
`$ bash setup.sh`  

### How to run file
`$ bash orderbook_collect.sh`

By default this will collect orderbook data for what is considered 'server0'. This value can be changed in orderbook_collect.sh'. 
*(At time of writing, not all servers have been made, so the result isn't an accurate representationof what symbols will be measured on Server 0)*

Note: If bash scripts are not working, you may need to perform an EOL conversion from Windows to Linux. This can be done through *Notepad++* under the Edit tab. This problem shouldn't crop up, however.

**EDIT: The bash script 'setup.sh' will only work for Debian-based distros because it contains the command 'apt-get install'. If using an RPM-based distro, use yum instead.**
