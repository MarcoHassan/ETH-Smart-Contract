from web3 import Web3
import json
import os

## Local node
class Node():

    def __init__(self, connectionAddress):

        self.web3 = Web3(Web3.HTTPProvider(connectionAddress))

        # Check if connected
        #self.web3.isConnected()
        #self.web3.eth.blockNumber


    def _getPrivateAccount(self, projectRoot, keystoreFile):

        walletPath = os.path.join(projectRoot, 'json', 'wallet.json')
        keystorePath = os.path.join(projectRoot, 'keystore', keystoreFile)

        with open(walletPath, "r") as file:
            walletJson = json.load(file)

        with open(keystorePath) as keyfile:
            keystoreFile = keyfile.read()

        #self.address = Web3.toChecksumAddress('aec95ca51e1ebf239c634c3fbd8767274cc13b7f')
        #private_key = web3.eth.account.privateKeyToAccount(private_key_account1)
        #private_key.address

        privateKey =  self.web3.eth.account.decrypt(keystoreFile, walletJson['Password'])

        return self.web3.eth.account.privateKeyToAccount(privateKey)

