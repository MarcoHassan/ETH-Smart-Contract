## Modules
import time
from pathlib import Path
from EthNode import *
from Logger import *

# Root path
projectRoot = Path(__file__).parents[2]

## Logger Set up
weatherLog = Logger(projectRoot)

## Node Connection -> Hosted (via Port) or Local (via URL)
conn = "https://rinkeby.infura.io/v3/133f7cb050074a1d93a87cc5fd64fcd6"      # "http://127.0.0.1:8080"
node = Node(conn)
weatherLog.logger.info(node.web3.isConnected())

## Get Private Key
account = 'Account2_PSSWD'      # Needs to match the Keyname of the Passwordvalue in the Wallet File and correspond to the Keystore file below
bidderKeystoreFile = 'UTC--2019-03-26T09-51-51.812264300Z--aec95ca51e1ebf239c634c3fbd8767274cc13b7f'
bidderPrivateAccount = node._getPrivateAccount(projectRoot, bidderKeystoreFile, account)

# -------------------------------------------------------------
## Bid in a currently Running Auction
with open(os.path.join(projectRoot, 'json', 'auction.json'), 'r') as infile:
    auction = json.load(infile)

auction_con = node.web3.eth.contract(
    abi=auction['abi'], address=auction['address'])

txn = auction_con.functions.bid().buildTransaction({'from': bidderPrivateAccount.address,
                                                    'value': node.web3.toWei(0.001, 'ether'),
                                                    'gas': 3000000,
                                                    'chainId': 4,
                                                    'nonce': node.web3.eth.getTransactionCount(bidderPrivateAccount.address)})

signed = bidderPrivateAccount.signTransaction(txn)
txn_hash = node.web3.eth.sendRawTransaction(signed.rawTransaction)

# Wait for the mining and save the transaction hash where the contract will be deployed on the Blockchain
time.sleep(25)
txn_receipt = node.web3.eth.waitForTransactionReceipt(txn_hash)


# -------------------------------------------------------------
## APPENDIX: Send ether from one Account to the Other
# from web3 import Web3
#
# def send_ether_to_contract(amount_in_ether, wallet_address, contract_address, wallet_private_key):
#
#     amount_in_wei = Web3.toWei(amount_in_ether, 'ether')
#
#     nonce = Web3.eth.getTransactionCount(wallet_address)
#
#     txn_dict = {
#         'to': contract_address,
#         'value': amount_in_wei,
#         'gas': 2000000,
#         'gasPrice': Web3.toWei('40', 'gwei'),
#         'nonce': nonce,
#         'chainId': 4  # 4 is the network ID for Rinkdin test Network
#     }
#
#     # wallet_private_key
#     signed_txn = Web3.eth.account.signTransaction(
#         txn_dict, wallet_private_key)
#
#     txn_hash = Web3.eth.sendRawTransaction(signed_txn.rawTransaction)
#
#     txn_receipt = None
#     count = 0
#     while txn_receipt is None and (count < 30):
#         txn_receipt = Web3.eth.getTransactionReceipt(txn_hash)
#         print(txn_receipt)
#         count += 10
#         time.sleep(10)
#
#     if txn_receipt is None:
#         return {'status': 'failed', 'error': 'timeout'}
#
#     return {'status': 'added', 'txn_receipt': txn_receipt}
#
#
# # Execute ETH coins transfer
# send_ether_to_contract(amount_in_ether, wallet_address, contract_address, wallet_private_key)