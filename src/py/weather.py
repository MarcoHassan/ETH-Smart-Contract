## Modules
from pathlib import Path
from solc import compile_files   # to compile Solidity code.
import time
from EthNode import *
from Logger import *

# Specify path
projectRoot = Path(__file__).parents[2]

## Logger Set up
weatherLog = Logger(projectRoot)

## Node Connection
# Connect to Hosted (via Port) or Local (via URL) node
# port = "http://127.0.0.1:8080"
infuraUrl = "https://rinkeby.infura.io/v3/133f7cb050074a1d93a87cc5fd64fcd6"
node = Node(infuraUrl)
weatherLog.logger.info(node.web3.isConnected())

## Get Private Key
auctioneerKeystoreFile = 'UTC--2019-03-26T09-31-53.436597400Z--50fcc57020a3fcb02974ba0d615b76e7161f56dc'
auctioneerPrivateAccount = node._getPrivateAccount(projectRoot, auctioneerKeystoreFile)

# -------------------------------------------------------------
## Create Weather Transfer Contracts in the Blockchain
contracts = ['lower_Weather_transfer', 'higher_Weather_transfer']

for contract in contracts:
    jsonFile = '.'.join([contract, 'json'])
    contractFilePath = os.path.splitdrive(os.path.join(projectRoot, 'src', 'sol', 'weather.sol'))[1]
    contractDirectPath = contractFilePath + ':' + contract
    # no colon ":" in Path (use "/Users/.." instead of "C:/Users/..." (https://github.com/ethereum/py-solc/issues/43)
    contracts = compile_files([contractFilePath])

    contract = node.web3.eth.contract(
        abi=contracts[contractDirectPath]['abi'],
        bytecode=contracts[contractDirectPath]['bin']
    )

    construct_txn = contract.constructor().buildTransaction(
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
    weather_contract = {}
    weather_contract['abi'] = contracts[contractDirectPath]['abi']
    weather_contract['address'] = txn_receipt.contractAddress

    # Parse weather_contract dictionary to .json file

    with open(os.path.join(projectRoot, 'json', jsonFile), 'w') as outfile:
        json.dump(weather_contract, outfile)


weatherLog.logger.info("Weather Contracts deployed into Blockchain")