## Step 1

Create python virtual environment where to download and save the packages of use.

```
$ virtualenv -p /usr/bin/python3.6 venv
```

#### Activate Virtual Environment

```
$ source venv/bin/activate
```

#### Install necessary Python Modules

```
$ pip3 install web3    // Download web3 to make use of javascript web3 API
       	       	       // and interact with the Ethereum Blockchain

$ pip3 isntall py-solc // To install python Solidity compiler

$ pip3 install time    // For the time.sleep function in order to wait for the necessary mining time

$ pip3 install python-forecastio // to use darkspy API and download weather data.
```

Moreover the python-solidity compiler package is dependent on the solidity compiler to be downloaded on the machine you are executing the program. To download the compiler you can choose one of the options available at [Solidity Compilers](https://solidity.readthedocs.io/en/v0.5.3/installing-solidity.html).

Important is however to notice that py-solc cannot synch with the newest Solidity compilers. We decided therefore to download the version 4.0.25 of the solidity compiler which is compatible with py-solc.

```
python -m solc.install v0.4.25

cp $HOME/.py-solc/solc-v0.4.25/bin/solc ~/venv/bin/       // copy the downloaded compiler to the virtual environment so that it is accessible.
```

#### Connection to Geth node

___________________
[Documentation for node connession](https://web3py.readthedocs.io/en/stable/providers.html#choosing-provider)
___________________


Using Geth Node Server it is possible to auto-connect to the node in automatic way thanks to the outstanding connectivity API integrated in web3 python method that leverages Javascript web3.js API.

```
from web3.auto import w3

w3.isConnected() ## check if automatic connession successful.
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


### Simple Weather Smart Contract

We decided finally to implement a simple smart contract leveraging the realized weather in a given location. The idea is to
connect through the **darkspy weather API**, get the actual weather and the apparent weather on a given location and to
execute a smart contract that transfer one ETH coin to the holder of the contract if the current weather is smaller equal to the
perceived weather at the selected location. We decided further to executing the contract each day at noon and midnight running a cornjob
on a DigitalOcean server.

#### Darkspy API

In order to leverage the darkspy API and download weather data it is necessary to register and obtain an API key.

______________
(darkspy API)[https://darksky.net/dev]
______________