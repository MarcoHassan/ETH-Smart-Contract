<div align="right">
Advanced Numerical Methods and Data Analysis - FS19-8,780
<br>
University of St. Gallen, 05.05.2019
<br>
</div>

-------------



# Ethereum Project

**Elisa Fleissner** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  elisa.fleissner@student.unisg.ch <br>
**Marco Hassan** &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  marco.hassan@student.unisg.ch <br>
**Lars Stauffenegger** &nbsp; &nbsp; &nbsp;lars.stauffenegger@student.unisg.ch  <br>
**Alexander Steeb** &nbsp;&nbsp; &nbsp; &nbsp; alexander.steeb@student.unisg.ch  <br>

## Introduction and project overview
In the project we decided to create an auction contract where people can bid to get the right on a 0.5 Ethereum transfer if the realized temperature in ```Rome``` is higher than the perceived temperature in the same city at a given hour.

In order to implement the above we leverage the **Solidity** language to write two smart contracts, one defining the conditions of the auction and a second to define the 0.5 Ethereum transfer to the auction higher bidder.  Moreover we leverage ```python scripts``` in order to connect to the Ethereum blockchain through the ```web3.py``` API. We tested and developed on Linux, Mac  and Windows environments using both local and hosted nodes.

In the specific the project structure can be summarized as follows and will be explained in detail in the sections below:

1. Install ```geth``` or setup an ```infura``` account, run a node on the rinkeby testnet and create accounts.

2. Get an API key from ```darkspy``` to withdraw actual and perceived weather information at a chosen location and install further python packages.

3. Write Solidity scripts.

4. Deploy the weather contracts specifying the Ethereum transfer to the highest bidder.

5. Deploy the auction contract starting the auction.

6. Run the ```deploy.py``` python script to check whether the bidding
period is still open and automatically transfer the 0.5 Ethereum coins
to the highest bidder if the auction time is over.

## Program Execution

Before entering the details of the code, let's briefly discuss the
nitty-gritty program execution.

#### Step 0: Connect to Ethereum blockchain via web3 python API

Explanation omitted. It will follow in the next sections.

#### Step 1: Deploy the weather smart contracts

```
(virtual environment).../src/py$ python3 WeatherTransfer.py
```

#### Step 2: Activate the auction

```
(virtual environment)..../src/py$ python3 AuctionSetup.py
```

#### Step 3: Wait for bidding time of the auction

#### Step 4: Automatically transfer 0.5 Ether if condition fulfilled to the highest bidder

```
(virtual environment)..../src/py$ python3 RunAuction.py
```

## Local Node: Geth installation and configuration

We refer to the documentation below to install ```geth```.

__________
[Geth installation](https://github.com/ethereum/go-ethereum/wiki/Installing-Geth)
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
to the running node. Important is moreover to choose a port for the
communications that is not in use and will not inhibit the
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

## Hosted Node: Infura
As an alternative to Geth, we also used the infura API to connect to a hosted node. Under the below link one can register for free to get a personal API key in form of a URL.
__________
[Infura Register](https://infura.io/register)
__________

## Personal Ethereum Prerequisites
Two wallets on the rinkeby network are needed to fully run this project. A folder named ```keystore``` on the main project level, where all other folders are, needs to be created and the two keystore files (“UTC---.3as45sdf8977…") have to be placed inside. Further, the full keystore filename of the wallet you wish to use as the auctioneer account needs to be defined in the three main python code (described further below) as ```auctioneerKeystoreFile``` and the one of the wallet you wish to use as the bidder needs to be defined in ```Bid.py``` as ```bidderKeystoreFile```. It is also necessary to create a ```wallet.json``` in the json folder and insert the passwords to enable the code the decryption of  the private keys later. The file has to look as follows:
```
{"Account1_PSSWD": "auctioneerPW", "Account2_PSSWD": "bidderPW"}
```

## Python configuration

Once either ```geth``` is properly configured or an infura account has been created, we turn to the python dependencies and modules downloads. Firstly, we create a python virtual environment where to download and save the packages of use.

```
$ virtualenv -p /usr/bin/python3.6 venv
```

It is then possible to activate the virtual environment and download the dependencies

```
$ source venv/bin/activate

$ pip3 install web3    // Download web3 to make use of JavaScript web3 API
       	       	       // and interact with the Ethereum Blockchain

$ pip3 install py-solc // To install python Solidity compiler

$ pip3 install time    // For the time.sleep function in order to wait for the necessary mining time

$ pip3 install python-forecastio // to use darkspy API and download weather data.
```

The python-solidity compiler package is dependent on the Solidity compiler on your local machine. You can choose the compiler version from one of the options available at [SolidityCompilers](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html). To make the ```solc``` package work properly, we recommend checking all [prerequisites](https://solidity.readthedocs.io/en/v0.4.24/installing-solidity.html) have been installed as especially for Windows there are C++ build tool required.

Important is however to notice that py-solc cannot synchronize with the newest Solidity compilers. We decided therefore to download the version 4.0.25 of the solidity compiler which is compatible with py-solc.

```
python -m solc.install v0.4.25

cp $HOME/.py-solc/solc-v0.4.25/bin/solc ~/venv/bin/       // copy the downloaded compiler to the virtual environment so that it is accessible.
```

## Solidity code

The three Solidity scripts that back our program are available under the ```src/sol``` repository in this Github page.

The lower temperature script is the script to transfer Ether to an account to be specified if the the realized temperature in a selected location is smaller-equal than the perceived one. The higher temperature script is the analogy of the first and transfers Ether just when the perceived temperature is lower than the realized temperature. Both are straightforward and an explanation of code is omitted.

The auction script is a revised version of the auction program
available at the official Solidity tutorial page.

__________
[Simple Auction](https://solidity.readthedocs.io/en/v0.4.21/solidity-by-example.html)
__________


## Connection To node

At this stage all of the necessary libraries are downloaded and the solidity scripts available.

We turn to the python web3 API to connect to the running node.

A documentation for the various connection possibilities is available at
___________________
[Documentation for node concussion](https://web3py.readthedocs.io/en/stable/providers.html#choosing-provider)
___________________

For Geth We decided to connect through the HTTP mode by connecting to the ```rpcport```. If you are running the python script on the same machine where your node is running, it is then possible to connect on the ```127.0.0.1``` localhost, otherwise the IP of the machine running the node should be specified.

```
conn = "http://127.0.0.1:8080" 
or 
conn = "https://rinkeby.infura.io/v3/133f7cb05007sdf987sdrr3d64fcd6"
self.web3 = Web3(Web3.HTTPProvider(conn))
```

Once we are connected to the Ethereum blockchain node it is possible to interact with it through the web3 API.

_________________________________
[Source decipher your private key](https://web3py.readthedocs.io/en/stable/web3.eth.account.html)
________________________________

We extract first the private keys of the two accounts in order to authenticate and interact with the Rinkeby node and authorize
transactions. As this is something we have to do multiple times in different scripts we decided to write a function in a class file to make it easily reusable.

```
    def _getPrivateAccount(self, projectRoot, keystoreFile, passwordAccount):

        walletPath = os.path.join(projectRoot, 'json', 'wallet.json')
        keystorePath = os.path.join(projectRoot, 'keystore', keystoreFile)

        with open(walletPath, "r") as file:
            walletJson = json.load(file)

        with open(keystorePath) as keyfile:
            keystoreFile = keyfile.read()

        privateKey = self.web3.eth.account.decrypt(keystoreFile, walletJson[passwordAccount])

        return self.web3.eth.account.privateKeyToAccount(privateKey)
```

## Python Scripts

This section briefly introduces and comments the python scripts necessary for running the auction and automatically transfer the coins to the highest bidder. We wrote two class -- ```EthNode.py``` and ```Logger.py``` -- that allow us to reuse the connection object and the log handling and for all three main scripts which are described below.

#### Python Script 1 - Weather Conditional ETH Transfer Contracts

The smart contract to deploy the ETH conditional transfer is compiled
and deployed in the ```WeatherTransfer.py``` script. In a first step, we establish a conenction via a node (local or hosted) that allows us to interact with the blockchain. We then start the deployment on the blockchain of the two weather contracts conditionally transferring money depending on the difference between the two input parameters. This is done by compiling the contract at first via the ```compile_files``` function imported from the ```py-solc``` library. This will result in the ```abi``` .json specification of the various contracts implemented in the Solidity script and their corresponding bytecodes necessary for running the contracts through ```EVM```. Given the byte code and the abi description it was then possible to
deploy the contract on the blockchain by leveraging web3 API function ```web3.eth.contract()```.

Here the contract is constructed through the ```<contractname>.constructor().buildTransaction()``` web3 function and the ```abi``` and the ```address``` of the deployed function are saved in a created .json file to interact at a later stage from a different code - i.e. when the auction will be instantiated and finished. These contracts can be reused and for any other auction following the same payout logic and do not need to be recreated unless one looses the address or the abi to interact with it.

#### Python Script 2 - Auction Contract

This second script ```AuctionSetup.py``` sets the auction contract up in the blockchain. This means that running the script from the shell will instantiate an auction for bidding on the 0,5 ETH transfer conditional on the weather conditions. The default parameters set in the script are the following:

____________
beneficiary = auctioneer account

bidding time = three hours
_____________


The two can be adjusted from the user and it is also possible to slightly alter the script to allow parameter definition in the shell execution of the program. The code is analogous to the one explained in the previous section and a detailed explanation of such is omitted. It is important moreover to save the ```abi``` and the ```address``` of the contract as in the previous case to interact with the auction contract, place bids, withdraw the bids and terminate the contract once the bidding time has expired. This contract is only usable exactly for this auction as it will be set to ```ended = True ``` once the bidding time is over. In contrast to the weather transfer contracts, this one here needs to be rerun to start a new auction.

#### Python Script 3 - Running an Auction with automatic Transfer
This will open the .json files where the auction contract address and ```abi``` documentation is saved, open such contract in web3 and check whether the auction is finished or running. Once the auction is terminated it will take the saved highest bidder address and automatically transfer 0.5 ```Ether``` from the actioneer's account to the address if the actual temperature in Rome is smaller equal than the ```perceived``` one. Finally the beneficiary of the auction, will receive the highest bid from the highest bidder address.

The contract uses the difference between the perceived and realized temperature in Rome which is collected from weather forecast servers via **darkspy weather API**. 
______________
[darkspy API](https://darksky.net/dev)
______________

Given the API it is possible to simply withdraw the data inserting the coordinates for the city of interest and save the current realized and perceived weather.

```
# Insert the coordinates of the city of choice. (Here Rome (IT)).
lat = 41.89193
lng = 12.51133

current_weather = forecastio.load_forecast(dark_api_key, lat, lng).currently()

# As solidity language does not support floaters to guarantee consistency among the blocks multiply the number by 100 to always obtain integers.
temp = int(current_weather.temperature * 100)
apparent_temp = int(current_weather.apparentTemperature * 100)

```


#### Python Script 4 - Bidding
Once the auction is running it is possible for the owner of the contract to make the ```abi``` and ```address``` publicly available such that people can connect to it and place bids. Below is a python code example for placing such bids once the
connection to the ethereum blockchain has been established and the contract successfully opened under the name of ```auction_con```.

```
txn = auction_con.functions.bid().buildTransaction({'from': bidderPrivateAccount.address,
                                                    'value': node.web3.toWei(0.001, 'ether'),
                                                    'gas': 3000000,
                                                    'chainId': 4,
                                                    'nonce': node.web3.eth.getTransactionCount(bidderPrivateAccount.address)})

signed = bidderPrivateAccount.signTransaction(txn)
txn_hash = node.web3.eth.sendRawTransaction(signed.rawTransaction)
```

As an appendix to the bidding code, we provide a simple function which can be used to send ETH from one account to another. It is handy to use with manual inputs when testing the auction with two accounts to make sure there is the funds are allocated as needed. The structure to send ETH via web3 API on the Ethereum blockchain is simple. We defined first a ```txn_dict``` python dictionary where we specified the parameters of the transaction, such as the amount of ```ether``` to transfer, the gas price for the fast execution of the contract, the gas limit etc. Especially important is to set the ```chainid``` correctly. A list referencing ```chainid``` is available at [ChainIDlink](https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids). In our case as we work on ```Rinkeby``` test network we selected a ```chainid``` of 4.

Once the dictionary is properly defined we authenticate the transaction through the sender ```privateKey``` previously stored and deploy the transaction on the blockchain through the ```web3.eth.sendRawTransaction()``` function saving moreover the
transaction hash in order to inspect the transaction at a later point on ```rinkeby explorer```. The final loop waits until the transaction has been mined and returns and error if the mining was unsuccessful.

## Final comments and ideas

To fully appreciate the project we recommend to run ```geth``` node on a server such that it will be running 24/7 and to instruct a few cronjobs to instantiate the auction and automatically transfer the coins.

For instance, we firstly executed the ```WeatherTransfer.py``` on the server as the script needs to run just a single time. We then set up two cron jobs, one instantiating the auction by running the ```AuctionSetup.py``` script at noon. And another cron job running the ```RunAuction.py``` contract at midnight.

In this case each day an auction will be instantiated at noon running for three hours where people can place bids to get the right on the 0.5 Ether transfer. Moreover the deploy script will run at noon checking if the difference of realized and perceived temperature in Rome is positive and automatically transferring the coins if the condition of the contract is fulfilled.

It is clear that the project above is highly scalable. It is theoretically possible to slightly alter the above and easily shift
the ```sports bids``` on the blockchain. A little bit of front-end development would then make the whole user friendly and potentially appetible to the general public.
