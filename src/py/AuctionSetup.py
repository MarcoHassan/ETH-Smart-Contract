## Modules
import time
from pathlib import Path
from solc import compile_files   # to compile Solidity code.

## Make sure your virtual environment is in the right directory to download the python defined modules.
import os
os.chdir(Path(__file__).parents[0])

from EthNode import *
from Logger import *

# Root path
projectRoot = Path(__file__).parents[2]

## Logger Set up
auctioneerLog = Logger(projectRoot)

## Node Connection -> Hosted (via Port) or Local (via URL)
conn = "https://rinkeby.infura.io/v3/133f7cb050074a1d93a87cc5fd64fcd6"      # "http://127.0.0.1:8080"
node = Node(conn)
auctioneerLog.logger.info(node.web3.isConnected())

## Get Private Key
account = 'Account1_PSSWD'      # Needs to match the Keyname of the Passwordvalue in the Wallet File and correspond to the Keystore file below
auctioneerKeystoreFile = 'UTC--2019-03-26T09-31-53.436597400Z--50fcc57020a3fcb02974ba0d615b76e7161f56dc'
auctioneerPrivateAccount = node._getPrivateAccount(projectRoot, auctioneerKeystoreFile, account)

# -------------------------------------------------------------
## Create Auction Contract in the Blockchain
contract = 'SimpleAuction'
contractFilePath = os.path.splitdrive(os.path.join(projectRoot, 'src', 'sol', 'auction.sol'))[1]
contractDirectPath = contractFilePath + ':' + contract
# no colon ":" in Path (use "/Users/.." instead of "C:/Users/..." (https://github.com/ethereum/py-solc/issues/43)
contracts = compile_files([contractFilePath])

contract = node.web3.eth.contract(
    abi=contracts[contractDirectPath]['abi'],
    bytecode=contracts[contractDirectPath]['bin']
)

# Three Hours
auctionDuration = 60*60*3

construct_txn = contract.constructor(_biddingTime=auctionDuration, _beneficiary=auctioneerPrivateAccount.address).buildTransaction(
    {
        'from': auctioneerPrivateAccount.address,
        'chainId': 4,
        'nonce': node.web3.eth.getTransactionCount(auctioneerPrivateAccount.address)
    })

# Authenticate and Upload the smart contract
signed_txn = auctioneerPrivateAccount.signTransaction(construct_txn)
txn_hash = node.web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Wait for the mining and save the transaction hash where the contract will be deployed on the Blockchain
time.sleep(25)
txn_receipt = node.web3.eth.waitForTransactionReceipt(txn_hash)

# Save contract 'address',  'abi' and 'bytecode' deploying the contract at a later stage.
auction_contract = {}
auction_contract['abi'] = contracts[contractDirectPath]['abi']
auction_contract['address'] = txn_receipt.contractAddress

# Write SimpleAuction Contract to .json file
with open(os.path.join(projectRoot, 'json', 'auction.json'), 'w') as outfile:
    json.dump(auction_contract, outfile)

auctioneerLog.logger.info("Auction was opened")


