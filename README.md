# Order Book Data Collection

During this stage of the project, data on the orderbooks of several coins on various exchanges will be collected continuously for an extended period of time. This data will later be used to backtest arbitrage trading strategies.

### Preliminary work
Before any data can be taken, trading accounts needed to be opened for the exchanges used. These were also verified in this stage as opposed to later due to some exchanges needing long waiting times to get verified on. The advantage to having a verified account instead of a basic account is higher daily withdrawal limits. Since arbitrage makes appreciable profit only with scale, large amounts of cryptocurrency may have to be moved on a daily basis.

### Preparing trading symbols to be used
Since there are 25 exchanges used in this program, with some having over 900 compatible trading pairs (or symbols), a script needed to be made to cross examine the trading symbols of all exchanges and keep the ones that have are shared by at least 2 exchanges, as only then would inter-exchange arbitrage be possible. These pairs would also have to exclude fiat pairings as fiat is not quick or cheap to withdraw. This script was aptly named ``'get_trading_symbols.py'``.
This script not only finds the active trading pairs shared among exchanges, it also serves to load the markets needed for ccxt by calling the loadMarkets() method for all the exchange objects. These objects are included in the dictionary returned by the script, along with the trading symbols for each exchange. The keys to this dictionary are simply the names of each exchange.

However, there are far too many trading symbols for a single Python program to collect data on without having gaps in data. For example, at time of writing the exchange HitBTC has 367 compatible trading symbols, while Kraken only has 20. If calls are made at the same rate, Kraken symbol data will be collected every few seconds while HitBTC symbol data will have gaps of up to several minutes at a time. The solution? **Many servers.** An issue presented with using lots of servers to collect data is: *How will the workload be split up?* That problem is solved with the script `'designate_workload.py'`, later changed to ``'initialise_exchanges.py'``. It takes a server number as an argument (servers will be named 'server1','server2', etc.) and returns which pairs should be used from a selection of servers. Some exchanges will get allocated different servers - it makes sense to base servers close geographically to exchanges. In the case of exchanges with a large number of pairs, they will just get most if not all servers to use. 
This script was named to ``'initialise_exchanges.py'`` as, with a few modifications it serves the purpose of preparing the data collection program for use.

Note: The work done in this step is found in the folder 'Symbols on exchanges'

### Collecting and saving data (with multithreading)

