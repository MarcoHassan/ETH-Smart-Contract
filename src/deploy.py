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

import forecastio                # to use darkspy API and get current weather data

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

#############################################
# Save Dark Spy Api key to get weather data #
#############################################

path_credentials = "/home/mhassan/Scrivania/ETH-Solidity/darkspy.json"

# Import your API credentials
with open(path_credentials, "r") as file:
    creds = json.load(file)

# Save Api key
dark_api_key = creds['API_KEY']


####################
# Get weather data #
####################

# Insert the coordinates of the city of choice. (Here Rome (IT)).
lat = 41.89193
lng = 12.51133

forecast = forecastio.load_forecast(dark_api_key, lat, lng)

current_weather = forecast.currently()

# As solidity language does not support floaters to guarantee consistency among the blocks multiply the number by 100 to always obtain integers.
temp = current_weather.temperature * 100

temp = int(temp)
temp

apparent_temp = current_weather.apparentTemperature * 100

apparent_temp = int(apparent_temp)
apparent_temp

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

# Get Geth endnode.
# if connected and web3.version.node.startswith('Geth'):
#    enode = web3.admin.nodeInfo['enode']

######################################################################
# Save Ethereum Wallet Accounts Passwords and store the private keys #
######################################################################

path_psswds = "/home/mhassan/Scrivania/ETH-Solidity/wallet.json"

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


###########################
# Deploy Auction contract #
###########################

# Parse weather_contract dictionary to .json file
with open('/home/mhassan/Scrivania/ETH-Solidity/auction.json', 'r') as infile:
    auction = json.load(infile)

auction_con = web3.eth.contract(
    abi=auction['abi'], address=auction['address'])

ended = False

while ended == False:
    logger.info('Auction is ended?: {}'.format(
        auction_con.functions.is_ended().call()
    ))

    logger.info('Time left: {}'.format(
        auction_con.functions.time_left().call()
    ))

    winner_bid = auction_con.functions.highestBidder_addr().call()

    logger.info('Highest bidder: {}'.format(
        winner_bid
    ))

    txn = auction_con.functions.auctionEnd().buildTransaction({'from': web3.eth.accounts[0],
                                                               'gas': 50000,
                                                               'chainId': 4,
                                                               'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])})

    signed = web3.eth.account.signTransaction(txn, private_key_account1)
    txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

    ended = auction_con.functions.is_ended().call()

    logger.info('Auction is ended?: {}'.format(
        ended
    ))

    time.sleep(60)


################################################################
## Deploy existent contract on the blockchain given the 'abi' ##
## description and the contract 'address'                     ##
################################################################

# Parse weather_contract dictionary to .json file
with open('/home/mhassan/Scrivania/ETH-Solidity/lower_weather_transfer.json', 'r') as infile:
    lower_weather = json.load(infile)

weather_lower = web3.eth.contract(
    abi=lower_weather['abi'], address=lower_weather['address'])

web3.eth.getBalance(web3.eth.accounts[0])
web3.eth.getBalance(web3.eth.accounts[1])

# Execute
txn = weather_lower.functions.temperature_send(winner_bid,
                                               temp, apparent_temp).buildTransaction({'from': web3.eth.accounts[0],
                                                                                      'value': web3.toWei(0.5, 'ether'),
                                                                                      'gas': 38000,
                                                                                      'chainId': 4,
                                                                                      'nonce': web3.eth.getTransactionCount(web3.eth.accounts[0])})

signed = web3.eth.account.signTransaction(txn, private_key_account1)
txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)

web3.eth.getBalance(web3.eth.accounts[0])
web3.eth.getBalance(web3.eth.accounts[1])

######################################
# Deploy higher temperature contract #
######################################

# Parse weather_contract dictionary to .json file
# with open('/home/mhassan/Scrivania/ETH-Solidity/higher_weather_transfer.json', 'r') as infile:
#    higher_weather = json.load(infile)
#
# weather_higher = web3.eth.contract(
#    abi=higher_weather['abi'], address=higher_weather['address'])
#
# web3.eth.getBalance(web3.eth.accounts[0])
# web3.eth.getBalance(web3.eth.accounts[1])
#
# Execute
# txn = weather_higher.functions.temperature_send(web3.eth.accounts[0],
#                                                temp, apparent_temp).buildTransaction({'from': web3.eth.accounts[1],
#                                                                                       'value': web3.toWei(0.5, 'ether'),
#                                                                                       'gas': 38000,
#                                                                                       'chainId': 4,
#                                                                                       'nonce': web3.eth.getTransactionCount(web3.eth.accounts[1])})
#
#signed = web3.eth.account.signTransaction(txn, private_key_account2)
#txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
#
# web3.eth.getBalance(web3.eth.accounts[0])
# web3.eth.getBalance(web3.eth.accounts[1])
#
##################
### Bid Example ##
##################
#
# txn = auction_con.functions.bid().buildTransaction({'from': web3.eth.accounts[1],
#                                                    'value': web3.toWei(1, 'ether'),
#                                                    'gas': 3000000,
#                                                    'chainId': 4,
#                                                    'nonce': web3.eth.getTransactionCount(web3.eth.accounts[1])})
#
#signed = web3.eth.account.signTransaction(txn, private_key_account2)
#txn_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
