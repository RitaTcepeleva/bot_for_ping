from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/aac0d8357c264d198c5c6b1d24ae5292'))

def get_currency(txn_hash):
    #trans_action = w3.eth.waitForTransactionReceipt(txn_hash)
    trans_v = w3.eth.getTransaction(txn_hash)
    trans_action = w3.eth.getTransactionReceipt(txn_hash)
    if len(trans_action.logs) == 6:
        curr_addr = trans_action.logs[2].address
        ret_amount = int(trans_action.logs[2].data, 16)/1000000000000000000
        amount = int(trans_v.value) / 1000000000000000000
    elif len(trans_action.logs) == 3:
        false_addr = trans_action.logs[2].topics[3].hex().split('x')
        curr_addr = '0x'+false_addr[1].lstrip('0')
        ret_amount = int(trans_action.logs[0].data, 16)/100000
        amount = int(trans_v.value) / 1000000000000000000
    #la = trans_action.logs[0].topics[1].hex()
    #ret_amount = int(trans_action.logs[2].data, 16)

    return curr_addr, ret_amount, amount

#tran = w3.eth.waitForTransactionReceipt('0xa7b44f81a8236443227e5372bba92c4976240104153d8820f66092edf9cb9467')

#lapenko_rulit = get_currency('0xbf281d23702a28ff7ebc8c3d93c2e2032da767b8691418cafd7efcfcf6bd0fc2')

#print(w3.eth.getTransaction('0xa7b44f81a8236443227e5372bba92c4976240104153d8820f66092edf9cb9467'))
