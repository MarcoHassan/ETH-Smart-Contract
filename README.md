# Ethereum Project

This is a project for the _Advanced Numerical Methods & Data Analysis_
course at the University of St. Gallen.

In the project we decided to create an auction contract where people
can bid to get the right on a 0.5 Ethereum transfer if the realized
temperature in ```Rome``` is higher than the perceived temperature in
the same city at a given hour.

In order to implement the above we leverage the **Solidity**
language to write two smart contracts, one defining the conditions of
the auction and a second to define the 0.5 Ethereum transfer to the
auction higher bidder.  Moreover we leverage ```python scripts``` in
order to connect to the Ethereum blockchain through the web3.js API.

In the specific the project structure can be summarized as follows and
will be explained in detail in the sections below:

1. Install ```geth```, run an node on the rinkeby testnet and create accounts.

2. Get an API key from ```darkspy``` to withdraw actual and perceived
weather at a chosen location and install further python packages.

3. Write Solidity Scripts.

4. Deploy the weather contracts specifying the Ethereum transfer to the highest bidder.

5. Deploy the auction contract starting the auction.

6. Run the ```deploy.py``` python script to check whether the bidding
period is still open and automatically transfer the 0.5 Ethereum coins
to the highest bidder if the auction time is over.

## Program Execution

Before entering the details of the code let's briefly discuss the
nitty-gritty program execution.

#### Step 0: Connect to Ethereum Blockchain via web3 python API

Explanation omitted. It will follow in the next sections.

#### Step 1: Deploy the weather smart contracts

```
(virtual environment).../src/py$ python3 weather.py
```

#### Step 2: Activate the Auction

```
(virtual environment)..../src/py$ python3 auction.py
```

#### Step 3: Wait for bidding time of the auction

#### Step 4: Automatically transfer 0.5 Ether if condition fulfilled to the highest bidder

```
(virtual environment)..../src/py$ python3 deploy.py
```

## Geth Installation and Configuration

We refer to the documentation below to install ```geth```.

__________
[Geth installation] (https://github.com/ethereum/go-ethereum/wiki/Installing-Geth)
__________

Once properly installed it is possible to connect a node on the rinkeby test network by running the following command.

```
geth --rinkeby --datadir=~/.ethereum --port=30304 --cache=2048
--rpc --rpcport=8080 --rpcapi=eth,web3,net,personal --syncmode=light
--bootnodes=enode://a24ac7c5484ef4ed0c5eb2d36620ba4e4aa13b8c84684e1b4aab0cebea2ae45cb4d375b77eab56516d34bfbd3c1a833fc51296ff084b770b94fb9028c4d25ccf@52.169.42.101:30303
```

This will instantiate the ```.ethereum``` directory in the home
directory. This will be of paramount importance as under such
directory the blocks will be downloaded and the private keys of the
accounts created.

Important is moreover to underline the choice of the
```rpcport```. This is important to remember for the web3 connection
to the running node. Important is moreover to choose for the
communications a port that is not in use and will not inhibit the
smooth communication with other networks.

Finally, the ```bootnodes``` parameter is of first order
importance in our case due to problematic end-nodes connection in the
light version - still experimental at the time of this writing -.

Once the command is run on Linux OS it will automatically download the
necessary blockchain history. When up to date it is then possible to
start developing.

As a first step we created two accounts by running the following
command and entering corresponding passwords.

```
geth --datadir=~/.ethereum account new
```

## Python Configuration

Once ```geth``` is properly configured we turned to the python
dependencies and modules downloads.

Firstly we created python virtual environment where to download and
save the packages of use.

```
$ virtualenv -p /usr/bin/python3.6 venv
```

It is then possible to activate the virtual environment and download
the dependencies

```
$ source venv/bin/activate

$ pip3 install web3    // Download web3 to make use of JavaScript web3 API
       	       	       // and interact with the Ethereum Blockchain

$ pip3 install py-solc // To install python Solidity compiler

$ pip3 install time    // For the time.sleep function in order to wait for the necessary mining time

$ pip3 install python-forecastio // to use darkspy API and download weather data.
```

The python-solidity compiler package is dependent on the solidity
compiler on your local machine. You can choose the compiler version
from one of the options available at [Solidity
Compilers](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html).

Important is however to notice that py-solc cannot synchronize with
the newest Solidity compilers. We decided therefore to download the
version 4.0.25 of the solidity compiler which is compatible with
py-solc.

```
python -m solc.install v0.4.25

cp $HOME/.py-solc/solc-v0.4.25/bin/solc ~/venv/bin/       // copy the downloaded compiler to the virtual environment so that it is accessible.
```

## Solidity Code

The three Solidity scripts that backs our program are available under
the ```src/sol``` repository in this Github page.

The lower temperature script is the script to transfer Ether to an
account to be specified if the the realized temperature in a selected
location is smaller-equal than the perceived one.

The higher temperature script is the analogy of the first and transfers
Ether just when the perceived temperature is lower than the realized
temperature.

Both are straightforward and an explanation of code is omitted.

The auction script is a revised version of the auction program
available at the official Solidity tutorial page

__________
[Simple Auction](https://solidity.readthedocs.io/en/v0.4.21/solidity-by-example.html)
__________


## Connection to Geth node

At this stage all of the necessary libraries are downloaded and the solidity scripts available.

We turn to the python web3 API to connect to the running node.

A documentation for the various connection possibilities is available at
___________________
[Documentation for node concussion](https://web3py.readthedocs.io/en/stable/providers.html#choosing-provider)
___________________

We decided to connect through the HTTP mode by connecting to the
```rpcport```. If you are running the python script on the same
machine where your node is running it is then possible to connect on
the ```127.0.0.1``` localhost, otherwise the IP of the machine running
the node should be specified.

```
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8080"))
```

Once we are connected to the Ethereum blockchain node it is possible
to interact with it through the web3 API.

We extract first the private keys of the two accounts in order to
authenticate and interact with the Rinkeby node and authorize
transactions.

_________________________________
[Source decipher your private key](https://web3py.readthedocs.io/en/stable/web3.eth.account.html)
________________________________

```
with open('~/.ethereum/rinkeby/keystore/<Account encrypted key; i.e. UTC--2019-03-30T11-11-56.210678255Z--903935ee0a8ed552d50523ebf465a8025c75c4cb>') as keyfile:
    encrypted_key = keyfile.read()
    private_key_account1 = w3.eth.account.decrypt(encrypted_key, 'YOUR ACCOUNT PSSWD')
```

## Python Scripts

This section briefly introduces and comments the python scripts
necessary for running the auction and automatically transfer the coins
to the highest bidder.

#### Python Script 1 - ETH Conditional Transfer Contracts

The smart contract to deploy the ETH conditional transfer is compiled
and deployed in the ```weather.py``` script.

We started the script with a general exercise to test the
connection and the web3 API functions. It consists of a simple
function defining an 1 ether transfer between the accounts.

The structure to operate via web3 API on the Ethereum blockchain is
simple. We defined first a ```txn_dict``` python dictionary where we
specified the parameters of the transaction, such as the amount of
```ether``` to transfer, the gas price for the fast execution of the
contract, the gas limit etc.

Especially important is to set the ```chainid``` correctly. A list
referencing ```chainid``` is available at [ChainID
link](https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids). In
our case as we work on ```Rinkeby``` test network we selected a
```chainid``` of 4.

Once the dictionary is properly defined we authenticate the
transaction through the sender ```private key``` previously stored and
deploy the transaction on the blockchain through the
```web3.eth.sendRawTransaction()``` function saving moreover the
transaction hash in order to inspect the transaction at a later point
on ```rinkeby explorer```.

The final loop waits until the transaction has been mined and returns
and error if the mining was unsuccessful.

After this general exercise and the explanation of the most important
web3 API functions we turned to the deployment on the blockchain of
the two weather contracts conditionally transferring money depending on
the difference between the two input parameters.

This is done by compiling the contract at first via the
```compile_files``` function imported from the ```py-solc```
library. This will result in the ```abi``` .json specification of the
various contracts implemented in the Solidity script and their
corresponding bytecodes necessary for running the contracts through
```EVM```.

Given the byte code and the abi description it was then possible to
deploy the contract on the blockchain by leveraging web3 API function
```web3.eth.contract()```.

From here on the passages are analogous to the one previously
mentioned in the case of the simple ether transfer with the difference
that the parameters of the transaction are specified when constructing
the contract through the ```<contract
name>.constructor().buildTransaction()``` web3 function.

Finally, we decide to save the ```abi``` and the ```address``` of the
deployed function in a created .json file to call the functions of the
contracts at a later stage - i.e. when the auction will be
instantiated and finished -.

#### Python Script 2 - Auction Initialization

This second script initializes the auction. This means that running
the script from the shell you will instantiate a auction for bidding
on the 0,5 ETH transfer conditional on the weather conditions.

The default parameters set in the script are the following:

____________
beneficiary = first account on the running geth node.

bidding time = three hours
_____________


The two can be adjusted from the user and it is also possible to
slightly alter the script to allow parameter definition in the shell
execution of the program.

The code is analogous to the one explained in the previous section and
a detailed explanation of such is omitted.

It is important moreover to save the ```abi``` and the ```address```
of the contract as in the previous case to interact with the auction
contract, place bids, withdraw the bids and terminate the contract
once the bidding time has expired.

#### Bid Example

Once the auction is running it is possible for the owner of the
contract to make the ```abi``` and ```address``` publicly available
such that people can connect to it and place bids.

Below is a python code example for placing such bids once the
connection to the ethereum blockchain has been established and the
contract successfully opened under the name of ```auction_con```.

```
 txn = auction_con.functions.bid().buildTransaction({'from': web3.eth.accounts[1],
                                                    'value': web3.toWei(1, 'ether'),
                                                    'gas': 3000000,
                                                    'chainId': 4,
                                                    'nonce': web3.eth.getTransactionCount(web3.eth.accounts[1])})

signed = web3.eth.account.signTransaction(txn, private_key_account2)
txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
```


#### Python Script 3 - ETH automatic transfer

Once the auction is running it is possible to run this final script.

This will open the .json files where the auction contract address and
```abi``` documentation is saved, open such contract in web3 and check
whether the auction is finished or running.

Once the auction is terminated it will take the saved highest bidder
address and automatically transfer 0.5 ```Ether``` from the geth node
first account to the address if the actual temperature in Rome is
smaller equal than the ```perceived``` one. Finally the beneficiary of
the auction, will receive the highest bid from the highest bidder
address.

As such contract leverages the difference between the perceived and
realized temperature in Rome it is necessary to collect the
information on python.

We decided to gather the information by connecting through the
**darkspy weather API** to the weather forecast servers and get the
information of interest.

#### Darkspy API - comment

In order to leverage the darkspy API and download weather data it is necessary to register and obtain an API key.

______________
[darkspy API](https://darksky.net/dev)
______________

Given the API it is possible to simply withdraw the data inserting the
coordinates for the city of interest and save the current realized and
perceived weather.

```
# Insert the coordinates of the city of choice. (Here Rome (IT)).
lat = 41.89193
lng = 12.51133

forecast = forecastio.load_forecast(dark_api_key, lat, lng)

current_weather = forecast.currently()

# As solidity language does not support floaters to guarantee consistency among the blocks multiply the number by 100 to always obtain integers.
temp = current_weather.temperature * 100

apparent_temp = current_weather.apparentTemperature * 100
```

## Final comments and ideas

To fully appreciate the project we recommend to run ```geth``` node on
a server such that it will be running 24/7 and to instruct a few
cronjobs to instantiate the auction and automatically transfer the
coins.

For instance, we firstly executed the ```weather.py``` on the server
as the script needs to run just a single time. We then set up two cron
jobs, one instantiating the auction by running the ```auction.py```
script at noon.And another cron job running the ```deploy.py```
contract at midnight.

In this case each day an auction will be instantiated at noon running
for three hours where people can place bids to get the right on the
0.5 Ether transfer. Moreover the deploy script will run at noon
checking if the difference of realized and perceived temperature in
Rome is positive and automatically transferring the coins if the
condition of the contract is fulfilled.

It is clear that the project above is highly scalable. It is
theoretically possible to slightly alter the above and easily shift
the ```sports bids``` on the blockchain. A little bit of front-end
development would then make the whole user friendly and potentially
appetible to the general public.