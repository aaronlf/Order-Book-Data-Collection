# Order Book Data Collection

During this stage of the project, data from the orderbooks of several coins on various exchanges will be collected continuously for an extended period of time. This data will later be used to backtest arbitrage trading strategies.

### Preliminary work
Before any data can be taken, trading accounts needed to be opened for the exchanges used. These were also verified in this stage as opposed to later due to some exchanges needing long waiting times to get verified with. The advantage to having a verified account instead of a basic account is a higher daily withdrawal limit. Since arbitrage makes appreciable profit only with scale, large amounts of cryptocurrency may have to be moved on a daily basis.

### Preparing trading symbols to be used
Since there are 25 exchanges used in this program, with some having over 900 compatible trading pairs (or symbols), a script needed to be made to cross-examine the trading symbols of all exchanges and keep the ones that have are shared by at least 2 exchanges, as only then would inter-exchange arbitrage be possible. These pairs would also have to exclude fiat pairings as fiat is not quick or cheap to withdraw. This script is aptly named ``'get_trading_symbols.py'``.
This script not only finds the active trading pairs shared among exchanges, it also serves to load the markets needed for ccxt by calling the loadMarkets() method for all the exchange objects. These objects are included in the dictionary returned by the script, along with the trading symbols for each exchange. The keys to this dictionary are simply the names of each exchange.

However, there are far too many trading symbols for a single Python program to collect data on without having gaps. For example, at time of writing the exchange HitBTC has 367 compatible trading symbols, while Kraken only has 20. If calls are made at the same rate, Kraken symbol data will be collected every few seconds while HitBTC symbol data will have gaps of up to several minutes at a time. The solution? **Many servers.** 

An issue presented with using lots of servers to collect data is: *How will the workload be split up?* That problem is solved with the script `'designate_workload.py'`, later changed to ``'initialise_exchanges.py'``. After importing the dictionary of exchanges and symbols from `'designate_workload.py'`, it takes a server number as an argument (servers will be named 'server0', 'server1', 'server2', etc.) and returns which pairs should be used on a selection of servers. Some exchanges will get allocated different servers - it makes sense to base servers close geographically to exchanges. In the case of exchanges with a large number of pairs, they will just get most if not all servers to use. 
This script was named to ``'initialise_exchanges.py'`` as, with a few modifications it serves the purpose of preparing the data collection program for use.

Note: The work done in this step is found in the folder 'Symbols on exchanges'

### Collecting and saving data (with multithreading)
In this step, live orderbook data is collected using API calls to various symbols as specified in `'initialise_exchanges.py'`. This orderbook information is stored as a 1 row-long Pandas dataframe with the columns "bid_price", "bid_volume", "ask_price", "ask_volume" and "timestamp". By checking the precision of the prices and volumes, the dtypes of the entries are converted from float64 to float32 to save space if possible. This dataframe is then appended or written (depending on if the file exists or not) to a hdf5 file named by the symbol and exchange. 

It's useful to have orderbook data from different exchanges collected at the same time. For this reason, data collection is done in parallel using the ``threading`` module. A function named 'schedule_tasks()' iterates through the list of symbols for a particular exchange every *rateLimit* seconds (where the rate limit is converted from ms to s), collecting the orderbook information for each symbol and saving to their respective h5 files. By iterating through all of the exchanges, a separate thread is created that runs this function. After all threads have been made, they are started and data is collected almost simultaneously for many trading pairs.
This program is named `orderbook.py`.

### Execution of program
This program will be set to go live on many different servers. For each `'initialise_exchanges.py'` script however, the value of 'server_number' will depend on what server the program is run from.

An important thing to consider when using CCXT is that they frequently update their code, often as a result of changing their API functionality. To ensure the version of CCXT being used is up-to-date, the Python program will be restarted about once a day or so. By using a simple bash script, a while loop can be made to run the Python program until a condition is met to call os._exit() (perhaps a separate thread is run that keeps track of time?), followed by `pip install ccxt --upgrade`.
