#############
## Modules ##
#############

# for autoconnect to the ethereum node and get IP and port of the server.
import os
from web3.auto import w3

import logging                    # for logging documentation
from web3 import Web3             # to connect to the Ethereum node
# from web3.contract import ConciseContract  # boohhh

from solc import compile_files   # to compile Solidity code.

# to allow for connectivity window for asyncronous execution of contracts given the mining time
import time

import json                      # to transfer info via .json

###################
## Logger Set up ##
###################

# Specify path
path_log = "/home/mhassan/Scrivania/ETH-Solidity/log/eth.log"

# Specify logger layout
logger = logging.getLogger('eth')
hdlr = logging.FileHandler(path_log)
formatter = logging.Formatter('%(asctime)s (%(levelname)s) - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)  # to get information from info and above

#################
## Connection  ##
#################

# Connect to blockchain
connected = w3.isConnected()

logger.info(connected)

# Get Geth endnode.
if connected and w3.version.node.startswith('Geth'):
    enode = w3.admin.nodeInfo['enode']

# Get Geth server IP and port
#help_list = enode.split('@')

# Connect to Geth node over the network
# web3 = Web3(WebsocketProvider("ws://" + help_list[1])

# web3=Web3(WebsocketProvider('ws://127.0.0.1:8546'))
# THE ABOVE IS NOT NECESSARY. ALREADY CONNECTED TO THE ENDNODE AUTOMATICALLY.

# Extract private key. Make sure to select the correct account.
with open('/home/mhassan/.ethereum/rinkeby/keystore/UTC--2019-03-30T11-11-56.210678255Z--903935ee0a8ed552d50523ebf465a8025c75c4cb') as keyfile:
    encrypted_key = keyfile.read()
    private_key_account1 = w3.eth.account.decrypt(encrypted_key, 'Password')

# Send coins


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


# Execute ETH coins transfer
send_ether_to_contract(
    1, w3.eth.accounts[0], w3.eth.accounts[1], wallet_private_key=private_key_account1)

##################################################
## Compile and Execute general purpose Contract ##
##################################################

contracts = compile_files(
    ['/home/mhassan/Scrivania/ETH-Solidity/src/greeting.sol'])

contract = w3.eth.contract(
    abi=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/greeting.sol:Greeter']['abi'],
    bytecode=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/greeting.sol:Greeter']['bin']
)

private_key = w3.eth.account.privateKeyToAccount(private_key_account1)

construct_txn = contract.constructor().buildTransaction(
    {'from': w3.eth.accounts[0],
     'chainId': 4,
     'nonce': w3.eth.getTransactionCount(private_key.address), })

# Authentificate the transaction with the private key of the user.
signed = private_key.signTransaction(construct_txn)

# Execute the smart contract
txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

# Wait for the mining and save the transaction hash where the contract will be deployed on the blockchain
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=txn_receipt.contractAddress,
    abi=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/greeting.sol:Greeter']['abi'],
)

# Display the default greeting from the contract
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))

# Execute
txn = greeter.functions.setGreeting('Robocop').buildTransaction({'from': w3.eth.accounts[0],
                                                                 'chainId': 4,
                                                                 'nonce': w3.eth.getTransactionCount(private_key.address), })

signed = w3.eth.account.signTransaction(txn, private_key_account1)
txn_hash = w3.eth.sendRawTransaction(signed.rawTransaction)


# Display the new greeting value
print('Updated contract greeting: {}'.format(
    greeter.functions.greet().call()
))
