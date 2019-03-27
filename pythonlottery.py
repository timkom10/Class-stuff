#!/usr/bin/python3


import json
import hashlib
import sys
from web3 import Web3, HTTPProvider, IPCProvider
from pprint import pprint

web3 = Web3 (HTTPProvider ("http://localhost:9545"))

# Read the ABI
with open ("abi.json") as f:
    abi = json.load (f)

# Get the contract address
if len (sys.argv) == 2:
    contract_address = sys.argv[1]
else:
    block_number = web3.eth.blockNumber
    contract_address = None
    while contract_address == None and block_number >= 0:
        block = web3.eth.getBlock (block_number)
        for tx_hash in block.transactions:
            tx = web3.eth.getTransactionReceipt (tx_hash)
            contract_address = tx.get ("contractAddress") 
            if contract_address != None:
                break
        block_number = block_number - 1
contract = web3.eth.contract (abi = abi, address = contract_address)
print ("Using contract address {:s}\n".format (contract_address))

# Play number 100 on account 1 (the second testrpc account) with random number 200.
account_index = 1
n = 100
r = 200
account = web3.eth.accounts[account_index]
print ("Using account {:d} with address {:s} to play on contract {:s}".format (account_index, account, contract_address))
# Compute the hash of n and r in a way that will match up with the example Solidity code above.
data = int.to_bytes (n, 32, "big") + int.to_bytes (r, 32, "big")
hash_nr = hashlib.sha256 (data).hexdigest ()
# Send 0.01 ETH when we call the smart contract function "play".
transaction_hash = contract.transact ({
    "from": account,
    "value": web3.toWei (0.1, "ether")
}).play (Web3.toBytes (hexstr = hash_nr));

account_index = 2
n = 200
r = 300
account = web3.eth.accounts[account_index]
print ("Using account {:d} with address {:s} to play on contract {:s}".format (account_index, account, contract_address))
# Compute the hash of n and r in a way that will match up with the example Solidity code above.
data = int.to_bytes (n, 32, "big") + int.to_bytes (r, 32, "big")
hash_nr = hashlib.sha256 (data).hexdigest ()
# Send 0.01 ETH when we call the smart contract function "play".
transaction_hash = contract.transact ({
    "from": account,
    "value": web3.toWei (0.1, "ether")
}).play (Web3.toBytes (hexstr = hash_nr));
account_index = 3
n = 100
r = 300
account = web3.eth.accounts[account_index]
print ("Using account {:d} with address {:s} to play on contract {:s}".format (account_index, account, contract_address))
# Compute the hash of n and r in a way that will match up with the example Solidity code above.
data = int.to_bytes (n, 32, "big") + int.to_bytes (r, 32, "big")
hash_nr = hashlib.sha256 (data).hexdigest ()
# Send 0.01 ETH when we call the smart contract function "play".
transaction_hash = contract.transact ({
    "from": account,
    "value": web3.toWei (0.1, "ether")
}).play (Web3.toBytes (hexstr = hash_nr));
# TODO: Should play using other accounts here.

def printBalances ():
    for acc in web3.eth.accounts:
        balance = web3.eth.getBalance (acc)
        print ("{:s} has {:.020f} ETH".format (acc, float (web3.fromWei (balance, "ether"))))
    print ()

print ()
printBalances ()

# Set the winning number to be 100.  Assumes contract was deployed by the first testrpc account.
account = web3.eth.accounts[0]
transaction_hash = contract.transact ({
    "from": account
}).winning (100);

# Reveal on account 1 using random number 200.
r = 200
account_index = 1
account = web3.eth.accounts[account_index]
print ("Using account {:d} with address {:s} to reveal on contract {:s}".format (account_index, account, contract_address))
transaction_hash = contract.transact ({
    "from": account
}).reveal (r);

r = 300
account_index = 3
account = web3.eth.accounts[account_index]
print ("Using account {:d} with address {:s} to reveal on contract {:s}".format (account_index, account, contract_address))
transaction_hash = contract.transact ({
    "from": account
}).reveal (r);

# TODO: Should reveal using other accounts here.

print ()
printBalances ()

# Finish up to distribute winnings.  Assumes contract was deployed by the first testrpc account.
account = web3.eth.accounts[0]
transaction_hash = contract.transact ({
    "from": account
}).done ();

print ()
printBalances ()
