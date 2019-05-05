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


    def _getPrivateAccount(self, projectRoot, keystoreFile, passwordAccount):

        walletPath = os.path.join(projectRoot, 'json', 'wallet.json')
        keystorePath = os.path.join(projectRoot, 'keystore', keystoreFile)

        with open(walletPath, "r") as file:
            walletJson = json.load(file)

        with open(keystorePath) as keyfile:
            keystoreFile = keyfile.read()

        privateKey = self.web3.eth.account.decrypt(keystoreFile, walletJson[passwordAccount])

        return self.web3.eth.account.privateKeyToAccount(privateKey)

