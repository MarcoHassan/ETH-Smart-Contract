## Modules
import time
from pathlib import Path
import forecastio                # to use darkspy API and get current weather data

## Make sure your virtual environment is in the right directory to download the python defined modules.
import os
os.chdir(Path(__file__).parents[0])

from EthNode import *
from Logger import *

# Root path
projectRoot = Path(__file__).parents[2]

## Logger Set up
auctionLog = Logger(projectRoot)

## Node Connection -> Hosted (via Port) or Local (via URL)
conn = "https://rinkeby.infura.io/v3/1234567890DUMMY"      # "http://127.0.0.1:8080"
node = Node(conn)
auctionLog.logger.info(node.web3.isConnected())

## Get Private Key
account = 'Account1_PSSWD'      # Needs to match the Keyname of the Passwordvalue in the Wallet File and correspond to the Keystore file below
auctioneerKeystoreFile = 'UTC--2019-03-26T09-31-53.436597400Z--50fcc57020a3fcb02974ba0d615b76e7161f56dc'
auctioneerPrivateAccount = node._getPrivateAccount(projectRoot, auctioneerKeystoreFile, account)

# -------------------------------------------------------------
## Run Auction Contract in the Blockchain
with open(os.path.join(projectRoot, 'json', 'auction.json'), 'r') as infile:
    auction = json.load(infile)

auction_con = node.web3.eth.contract(
    abi=auction['abi'], address=auction['address'])

ended = False

while ended == False:
    ended = auction_con.functions.is_ended().call()
    auctionLog.logger.info('Auction is ended?: {}'.format(
        ended
    ))

    auctionLog.logger.info('Time left: {}'.format(
        auction_con.functions.time_left().call()
    ))

    winner_bid = auction_con.functions.highestBidder().call()
    winner_amount = auction_con.functions.highestBid().call()

    auctionLog.logger.info('Current highest bidder and amount: {}, {}'.format(
        winner_bid, node.web3.fromWei(winner_amount, 'ether')
    ))

    if ended == True:
        txn = auction_con.functions.auctionEnd().buildTransaction({'from': auctioneerPrivateAccount.address,
                                                               'gas': 50000,
                                                               'chainId': 4,
                                                               'nonce': node.web3.eth.getTransactionCount(auctioneerPrivateAccount.address)})

        signed = auctioneerPrivateAccount.signTransaction(txn)
        txn_hash = node.web3.eth.sendRawTransaction(signed.rawTransaction)



    auctionLog.logger.info('Auction is ended?: {}'.format(
        ended
    ))

    time.sleep(60*60)

# -------------------------------------------------------------
## Get Weather Data from Darkspy API
with open(os.path.join(projectRoot, 'json', 'darkspy.json'), 'r') as file:
    dark_api_key = json.load(file)['API_KEY']

# Insert the coordinates of the city of choice. (Here Rome (IT)).
lat = 41.89193
lng = 12.51133

current_weather = forecastio.load_forecast(dark_api_key, lat, lng).currently()

# As solidity language does not support floaters to guarantee consistency among the blocks multiply the number by 100 to always obtain integers.
temp = int(current_weather.temperature * 100)
auctionLog.logger.info("Actual temperature in Rome is: " + str(temp))

apparent_temp = int(current_weather.apparentTemperature * 100)
auctionLog.logger.info("Perceived temperature in Rome is: " + str(apparent_temp))

# -------------------------------------------------------------
## Run the Transfer Contract
payment = 0.025
contract = 'lower_weather'     # 'higher_Weather'

with open(os.path.join(projectRoot, 'json', '_'.join([contract, 'transfer.json'])), 'r') as infile:
    contract = json.load(infile)

weather_lower = node.web3.eth.contract(
    abi=contract['abi'], address=contract['address'])

# check Balance: node.web3.eth.getBalance(auctioneerPrivateAccount.address)

txn = weather_lower.functions.temperature_send(winner_bid,
                                               temp, apparent_temp).buildTransaction({'from': auctioneerPrivateAccount.address,
                                                                                      'value': node.web3.toWei(payment, 'ether'),
                                                                                      'gas': 38000,
                                                                                      'chainId': 4,
                                                                                      'nonce': node.web3.eth.getTransactionCount(auctioneerPrivateAccount.address)})

signed = auctioneerPrivateAccount.signTransaction(txn)
txn_hash = node.web3.eth.sendRawTransaction(signed.rawTransaction)
auctionLog.logger.info("Weather Transfer Contract Executed.")