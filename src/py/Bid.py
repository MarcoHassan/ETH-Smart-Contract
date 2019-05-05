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
