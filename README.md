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

$ pip3 install time    // For the time.sleep function
```

#### Connection to Geth node

___________________
(Documentation for node connession)[https://web3py.readthedocs.io/en/stable/providers.html#choosing-provider]
___________________


Using Geth Node Server it is possible to auto-connect to the node in automatic way thanks to the outstanding connectivity API integrated in web3 python method that leverages Javascript web3.js API.

```
from web3.auto import w3

w3.isConnected()
```

#### Extract your private key

To interact with Rinkeby node and authorize transactions it is necessary to authentificate through the usage of account private keys.
_________________________________
(Source decrypt your private key)[https://web3py.readthedocs.io/en/stable/web3.eth.account.html]
________________________________

In order to do that we decided to extract the ```.json``` file containing the informations regarding the private keys of the account of interest through the following method

```
with open('~/.ethereum/rinkeby/keystore/<Account encrypted key; i.e. UTC--2019-03-30T11-11-56.210678255Z--903935ee0a8ed552d50523ebf465a8025c75c4cb>') as keyfile:
    encrypted_key = keyfile.read()
    private_key_account1 = w3.eth.account.decrypt(encrypted_key, 'YOUR ACCOUNT PSSWD')
```

#### Transfer of ETH coins

Once the connection to the node has been established and the private keys extracted it is possible to define a function leveraging the web3 API to transfer Ethereum coins from one account to the next.

The code looks as follows, and especially important is to set the ```chainid``` correctly. A list referencing ```chainid``` is available at (ChainID link)[https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids]. In our case as we work on ```Rinkeby``` test network we selected a ```chainid``` of 4.

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

