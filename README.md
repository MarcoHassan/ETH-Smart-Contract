# Ethereum Project

This is a project for the _Advanced Numerical Methods & Data Analysis_ course at the University of St. Gallen.

In the project we decided to create an auction contract where people can bid to get the right on a 0.5 Ethereum
transfer if the realized temperature in ```Rome``` is higher than the perceived temperature in the same city at a given hour.

In order for to implement the above we leverage the **Solidity** language to write two smart contracts, one
defining the conditions of the auction and a second to define the 0.5 Ethereum transfer to the auction higher bidder.
Moreover we leverage ```python scripts``` in order to connect to the Ethereum blockchain through the web3.js API.

In the specific the project structure can be summarized as follows and will be explained in detail in the sections below:

1. Install ```geth```, run an node on the rinkeby testnet and create accounts through web3.js API.

2. Get an API key from ```darkspy``` to withdraw actual and perceived weather at a chosen location and install further python packages.

3. Write Solidity Scripts.

4. Deploy the weather contracts specifying the Ethereum transfer to the highest bidder.

5. Deploy the auction contract starting the auction.

6. Run the ```deploy.py``` python script to check whether the bidding period is still open and automatically transfer the 0.5 Ethereum coins to the highest bidder if the auction time is over.

## Geth Installation and Configuration

We refer to the documenation below to install ```geth```.

__________
[Geth installation] (https://github.com/ethereum/go-ethereum/wiki/Installing-Geth)
__________

Once properly installed it is possible to connect a node on the rinkeby test network by running the following command.

```
geth --rinkeby --datadir=~/.ethereum --port=30304 --cache=2048 --rpc --rpcport=8080 --rpcapi=eth,web3,net,personal --syncmode=light --bootnodes=enode://a24ac7c5484ef4ed0c5eb2d36620ba4e4aa13b8c84684e1b4aab0cebea2ae45cb4d375b77eab56516d34bfbd3c1a833fc51296ff084b770b94fb9028c4d25ccf@52.169.42.101:30303
```
This will instantiate the ```.ethereum``` directory in the home directory. This will be of paramount importance as under such directory the blocks will be
installed and the private keys of the accounts created.

Imporant is moreover to underline the chose ```rpcport```. This is important to remember for the later web3 connession to the running node. Important is
moreoveer to choose free ports for the communications without inhibiting the smooth communication with other networks.

Finally, the ```bootnodes``` parameter provided to be of first order importance in our case due to problematic endnodes connection in the light version
- still experimental at the time of this writing -.

Once the command is run on Linux OS it will automatically download some of the blockchain history. When up to date it is then possible to start developing.

As a first step we created two accounts by running the following command and entering a corresponding password.

```
geth --datadir=~/.ethereum account new
```

## Python Configuration

Once ```geth``` is properly configured we truned to the python dependencies and modules downloads.

Firstly we created python virtual environment where to download and save the packages of use.

```
$ virtualenv -p /usr/bin/python3.6 venv
```

It is then possible to activate the virtual environment and download the depencies

```
$ source venv/bin/activate

$ pip3 install web3    // Download web3 to make use of javascript web3 API
       	       	       // and interact with the Ethereum Blockchain

$ pip3 isntall py-solc // To install python Solidity compiler

$ pip3 install time    // For the time.sleep function in order to wait for the necessary mining time

$ pip3 install python-forecastio // to use darkspy API and download weather data.
```

The python-solidity compiler package is dependent on the solidity compiler on your local machine. You can choose the compiler version from one of the options available at [Solidity Compilers](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html).

Important is however to notice that py-solc cannot synch with the newest Solidity compilers. We decided therefore to download the version 4.0.25 of the solidity compiler which is compatible with py-solc.

```
python -m solc.install v0.4.25

cp $HOME/.py-solc/solc-v0.4.25/bin/solc ~/venv/bin/       // copy the downloaded compiler to the virtual environment so that it is accessible.
```

## Solidity Code

The three Solidity scripts that backs our program are available under the ```src/sol``` repository in this Github page.

The lower temperature script is the script to transfer Ether to an account to be specified if the
the realized temperature in a selected location is smaller-equal than the perceived one.

The higher temperature script is the analogy of the first and transfer Ether just when the perceived temperature is lower than the
realized temperature.

Both are straightforward and an explanation is omitted.

The auction script is a revised verision taken from the offical Solidity tutorial page available at

__________
[Simple Auction](https://solidity.readthedocs.io/en/v0.4.21/solidity-by-example.html)
__________


## Connection to Geth node

At this stage all of the necessary libraries are downloaded and we turn to the python web3 API to connect to the running node.

A documenation for the various connession possibilities is available at
___________________
[Documentation for node connession](https://web3py.readthedocs.io/en/stable/providers.html#choosing-provider)
___________________

We decided to connect through the HTTP mode by connecting to the ```rpcport```. If you are running the python script on the same
machine where your node is running it is then possible to connect on the ```127.0.0.1``` localhost, otherwise the IP of the machine running
the node should be specified.

```
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8080"))
```

#### Extract your private key

To interact with Rinkeby node and authorize transactions it is necessary to authentificate through the usage of account private keys.
_________________________________
[Source decrypt your private key](https://web3py.readthedocs.io/en/stable/web3.eth.account.html)
________________________________

In order to do that we decided to extract the ```.json``` file containing the informations regarding the private keys of the account of interest through the following method

```
with open('~/.ethereum/rinkeby/keystore/<Account encrypted key; i.e. UTC--2019-03-30T11-11-56.210678255Z--903935ee0a8ed552d50523ebf465a8025c75c4cb>') as keyfile:
    encrypted_key = keyfile.read()
    private_key_account1 = w3.eth.account.decrypt(encrypted_key, 'YOUR ACCOUNT PSSWD')
```

#### Transfer of ETH coins

Once the connection to the node has been established and the private keys extracted it is possible to define a function leveraging the web3 API to transfer Ethereum coins from one account to the next.

The code looks as follows, and especially important is to set the ```chainid``` correctly. A list referencing ```chainid``` is available at [ChainID link](https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids). In our case as we work on ```Rinkeby``` test network we selected a ```chainid``` of 4.

```
def send_ether_to_contract(amount_in_ether, wallet_address, contract_address, wallet_private_key):

    amount_in_wei = w3.toWei(amount_in_ether, 'ether')

    nonce = w3.eth.getTransactionCount(wallet_address)

    txn_dict = {
        'to': contract_address,
        'value': amount_in_wei,
        'gas': 2000000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
        'chainId': 4  # 4 is the network ID for Rinkdin test Network
    }

    # wallet_private_key
    signed_txn = w3.eth.account.signTransaction(
        txn_dict, wallet_private_key)

    txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    txn_receipt = None
    count = 0
    while txn_receipt is None and (count < 30):

        txn_receipt = w3.eth.getTransactionReceipt(txn_hash)

        print(txn_receipt)

        time.sleep(10)

    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    logger.info("%d Ethereum were transfered form accound %s to contract %s" % (
        amount_in_ether, wallet_address, contract_address))
    return {'status': 'added', 'txn_receipt': txn_receipt}
```

Finally to execute the Ethereum transfer you can simply enter the necessary informations, also leveraging the w3 opened connession to select the account of interest. Necessary at this point is nonetheless that you enter the decrypted private key of the account executing the transfer

```
send_ether_to_contract(1, w3.eth.accounts[0], w3.eth.accounts[1], wallet_private_key=private_key_account1)
```

## Contract Example

### Simple Weather Smart Contract

We decided finally to implement a simple smart contract leveraging the realized weather in a given location. The idea is to
connect through the **darkspy weather API**, get the actual weather and the apparent weather on a given location and to
execute a smart contract that transfer one ETH coin to the holder of the contract if the current weather is smaller equal to the
perceived weather at the selected location. We decided further to executing the contract each day at noon and midnight running a cornjob
on a DigitalOcean server.

#### Darkspy API

In order to leverage the darkspy API and download weather data it is necessary to register and obtain an API key.

______________
[darkspy API](https://darksky.net/dev)
______________

Given the API it is possible to simply withdraw the data inserting the coordinates for the city of interest and save the current realized and
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

#### Smart Contract - Compile and Execute

Given the actual weather realization and the apparent weather it is possible to compile a solidity contract in the python script
through the py-solc package installed and execute it by signing the trasaction with your private key and upload it on the public blockchain ledger.

```
# Compile Contract
contracts = compile_files(
    ['/home/mhassan/Scrivania/ETH-Solidity/src/weather.sol'])

# Save .json and binary code for the compiled contract.
contract = w3.eth.contract(
    abi=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/weather.sol:Weather_transfer']['abi'],
    bytecode=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/weather.sol:Weather_transfer']['bin']
)

## Save private key and address
private_key = w3.eth.account.privateKeyToAccount(private_key_account1)

construct_txn = contract.constructor().buildTransaction(
    {'from': w3.eth.accounts[0],
     'chainId': 4, ## Is rinkeby test network
     'nonce': w3.eth.getTransactionCount(private_key.address)})

# Authentificate the transaction with the private key of the user.
signed_txn = private_key.signTransaction(construct_txn)

# Execute the smart contract
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the mining and save the transaction hash where the contract will be deployed on the blockchain
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
```

Given the above it is then possible to deploy the contract and call its functions, in the specific the temperature_send function
that transfers ETH coins according to the actual vs. perceived weather as described above.

```
# Create the contract instance with the newly-deployed address
weather = w3.eth.contract(
    address=txn_receipt.contractAddress,
    abi=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/greeting.sol:Weather_transfer']['abi'],
)

# Execute
txn = weather.functions.temperature_send(w3.eth.accounts[1], 1,
                                         temp, apparent_temp).buildTransaction({'from': w3.eth.accounts[0],
                                                                                'chainId': 4,
                                                                                'nonce': w3.eth.getTransactionCount(private_key.address)})

signed = w3.eth.account.signTransaction(txn, private_key_account1)
txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
```