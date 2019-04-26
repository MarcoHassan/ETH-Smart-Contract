#############
## Modules ##
#############

import logging                   # for logging documentation
from web3 import Web3            # to connect to the Ethereum node
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

# Connect through HTTP node endpoint
# adapted the connession here --> localhost and port 8080 specified here
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8080"))

# Check if web3.auto managed to autoconnect to end node.
connected = web3.isConnected()
connected
logger.info(connected)

######################################################################
# Save Ethereum Wallet Accounts Passwords and store the private keys #
######################################################################

path_psswds = "/home/mhassan/Scrivania/ETH-Solidity/json/wallet.json"

# Import your API credentials
with open(path_psswds, "r") as file:
    psswds = json.load(file)

# Extract private key. Make sure to select the correct account.
with open('/home/mhassan/.ethereum/keystore/UTC--2019-04-22T07-18-39.263595338Z--0c1af8a8f69492b0e6984148992871c918df36f1') as keyfile:
    encrypted_key = keyfile.read()
    private_key_account1 = web3.eth.account.decrypt(
        encrypted_key, psswds['Account1_PSSWD'])

# Repete for the second contract
with open('/home/mhassan/.ethereum/keystore/UTC--2019-04-22T07-18-58.389017440Z--b8d031bd8e749b8258d25bfbfbb7409669434197') as keyfile:
    encrypted_key = keyfile.read()
    private_key_account2 = web3.eth.account.decrypt(
        encrypted_key, psswds['Account2_PSSWD'])

##############
# Send coins #
##############


def send_ether_to_contract(amount_in_ether, wallet_address, contract_address, wallet_private_key):

    amount_in_wei = web3.toWei(amount_in_ether, 'ether')

    nonce = web3.eth.getTransactionCount(wallet_address)

    txn_dict = {
        'to': contract_address,
        'value': amount_in_wei,
        'gas': 2000000,
        'gasPrice': web3.toWei('40', 'gwei'),
        'nonce': nonce,
        'chainId': 4  # 4 is the network ID for Rinkdin test Network
    }

    # wallet_private_key
    signed_txn = web3.eth.account.signTransaction(
        txn_dict, wallet_private_key)

    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    txn_receipt = None
    count = 0
    while txn_receipt is None and (count < 30):
        txn_receipt = web3.eth.getTransactionReceipt(txn_hash)
        print(txn_receipt)
        count += 10
        time.sleep(10)

    if txn_receipt is None:
        return {'status': 'failed', 'error': 'timeout'}

    logger.info("%d Ethereum were transfered form accound %s to contract %s" % (
        amount_in_ether, wallet_address, contract_address))
    return {'status': 'added', 'txn_receipt': txn_receipt}


# Execute ETH coins transfer
send_ether_to_contract(
    1, web3.eth.accounts[0], web3.eth.accounts[1], wallet_private_key=private_key_account1)


#####################################
# Create lower temperature contract #
#####################################

contracts = compile_files(
    ['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol'])

contract = web3.eth.contract(
    abi=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol:lower_Weather_transfer']['abi'],
    bytecode=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol:lower_Weather_transfer']['bin']
)

private_key = web3.eth.account.privateKeyToAccount(private_key_account1)

construct_txn = contract.constructor().buildTransaction(
    {'from': web3.eth.accounts[0],
     'chainId': 4,
     'nonce': web3.eth.getTransactionCount(private_key.address)})

# Authentificate the transaction with the private key of the user.
signed_txn = private_key.signTransaction(construct_txn)

# Execute the smart contract
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the mining and save the transaction hash where the contract will be deployed on the blockchain
txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)

# Save contract 'address',  'abi' and 'bytecode' deploying the contract at a later stage.
weather_contract = {}

weather_contract['abi'] = contracts['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol:lower_Weather_transfer']['abi']

weather_contract['address'] = txn_receipt.contractAddress

# Parse weather_contract dictionary to .json file
with open('/home/mhassan/Scrivania/ETH-Solidity/json/lower_weather_transfer.json', 'w') as outfile:
    json.dump(weather_contract, outfile)


########################################################
# Repeat the above for the higher_temperature contract #
########################################################

contracts = compile_files(
    ['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol'])

contract = web3.eth.contract(
    abi=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol:higher_Weather_transfer']['abi'],
    bytecode=contracts['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol:higher_Weather_transfer']['bin']
)

private_key = web3.eth.account.privateKeyToAccount(private_key_account1)

construct_txn = contract.constructor().buildTransaction(
    {'from': web3.eth.accounts[0],
     'chainId': 4,
     'nonce': web3.eth.getTransactionCount(private_key.address)})

# Authentificate the transaction with the private key of the user.
signed_txn = private_key.signTransaction(construct_txn)

# Execute the smart contract
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the mining and save the transaction hash where the contract will be deployed on the blockchain
txn_receipt = web3.eth.waitForTransactionReceipt(txn_hash)

# Save contract 'address',  'abi' and 'bytecode' deploying the contract at a later stage.
weather_contract = {}

weather_contract['abi'] = contracts['/home/mhassan/Scrivania/ETH-Solidity/src/sol/weather.sol:higher_Weather_transfer']['abi']

weather_contract['address'] = txn_receipt.contractAddress

# Parse weather_contract dictionary to .json file
with open('/home/mhassan/Scrivania/ETH-Solidity/json/higher_weather_transfer.json', 'w') as outfile:
    json.dump(weather_contract, outfile)
