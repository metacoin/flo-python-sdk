## Connect to FLO RPC
## Send an appdata message using a library function
## This requires a connection to a local running FLO node
# Special thanks: MustyMouse
# Special thanks: technanner

import pprint
import requests 
import os
import traceback

## TODO: Versioning 

## Library functions
# Get info from FLO RPC using getinfo call 
# This function is the basis for all getinfo sub-functions
def get_info():
    payload = b'{"jsonrpc":"1.0","id":"curltext","method":"getinfo","params":[]}'
    headers = {'content-type': 'text/plain'}
    return call_rpc(payload, headers)

def get_account_address(account):
    payload = b'{"jsonrpc":"1.0","id":"curltext","method":"getaccountaddress","params":[""]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']),
            data=payload, 
            headers=headers,
            auth=(os.environ['FLO_RPCUSER'],
            os.environ['FLO_PASSWORD'])
    )
    if r.json()['error'] is not None: 
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']
def write_to_blockchain(address, appdata=None):
    # TODO: figure out str.format() instead of concat
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"sendtoaddress","params":["' + address + '", 0.1, "", "", "' + appdata + '"]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

## Driver function
def call_rpc(payload, headers=None):
    if headers is None: headers = {'content-type': 'text/plain'}
    try:
        response = rpc_request(payload, headers)
        print "** RESPONSE **"
        print response
        return response
    except Exception as e:
        print traceback.print_exc(e)

def rpc_request(payload, headers):
    print "in rpc_request"
    headers = {'content-type': 'text/plain'}
    try: 
        r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    except Exception as e:
        print "rpc_request: exception"
        raise Exception(e)
    else: 
        if r.status_code == 401: raise Exception("[FLO SDK Exception]: 401 authentication failed on RPC request POST.")
        if r.json()['error'] is not None:
            print "rpc_request: error is not none"
            raise Exception("[FLO SDK Exception]: FLO RPC returned this error: " + r.json()['error'])
        else:
            print "rpc_request: error is none, returning the result"
            return r.json()['result']

## Blockchain
# getbestblockhash
# ================
# Returns the hash of the best (tip) block in the longest block chain.
# 
# Result
# "hex" (string) the block hash hex encoded
# 
# Examples
# > florincoin-cli getbestblockhash 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getbestblockhash", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_best_blockhash():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getbestblockhash","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getblock (hash, verbose)
# ========================
# If verbose is false, returns a string that is serialized, hex-encoded data for block 'hash'.
# If verbose is true, returns an Object with information about block <hash>.
# 
# Arguments:
# 1. "hash" (string, required) The block hash
# 2. verbose (boolean, optional, default=true) true for a json object, false for the hex encoded data
# 
# Result (for verbose = true):
# {
# "hash" : "hash", (string) the block hash (same as provided)
# "confirmations" : n, (numeric) The number of confirmations, or -1 if the block is not on the main chain
# "size" : n, (numeric) The block size
# "height" : n, (numeric) The block height or index
# "version" : n, (numeric) The block version
# "merkleroot" : "xxxx", (string) The merkle root
# "tx" : [ (array of string) The transaction ids
# "transactionid" (string) The transaction id
# ,...
# ],
# "time" : ttt, (numeric) The block time in seconds since epoch (Jan 1 1970 GMT)
# "nonce" : n, (numeric) The nonce
# "bits" : "1d00ffff", (string) The bits
# "difficulty" : x.xxx, (numeric) The difficulty
# "previousblockhash" : "hash", (string) The hash of the previous block
# "nextblockhash" : "hash" (string) The hash of the next block
# }
# 
# Result (for verbose=false):
# "data" (string) A string that is serialized, hex-encoded data for block 'hash'.
# 
# Examples:
# > florincoin-cli getblock "0c3b2c31c8aa025e5ae7a87dfe63d1795a061b95e7b00aee61e5384338a26739"
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["51809bec7b4ce59d29a26779f8c8d08fa36ec3aa76c9a042cda1eeb87ec01865"] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_block(blockhash, verbose=True):
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getblock","params":["' + blockhash + '", ' + str(verbose).lower() + ']}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getblockcount
# =============
# Returns the number of blocks in the longest block chain.
# 
# Result:
# n (numeric) The current block count
# 
# Examples:
# > florincoin-cli getblockcount 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockcount", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_block_count():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getblockcount","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']
    
# getblockhash (index)
# ====================
# Returns hash of block in best-block-chain at index provided.
# 
# Arguments:
# 1. index (numeric, required) The block index
# 
# Result:
# "hash" (string) The block hash
# 
# Examples:
# > florincoin-cli getblockhash 1000
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [1000] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_block_hash(index):
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getblockhash","params":[' + str(index) +']}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getchaintips
# ============
# Return information about all known tips in the block tree, including the main chain as well as orphaned branches.
# 
# Result:
# [
# {
# "height": xxxx, (numeric) height of the chain tip
# "hash": "xxxx", (string) block hash of the tip
# "branchlen": 0 (numeric) zero for main chain
# "status": "active" (string) "active" for the main chain
# },
# {
# "height": xxxx,
# "hash": "xxxx",
# "branchlen": 1 (numeric) length of branch connecting the tip to the main chain
# "status": "xxxx" (string) status of the chain (active, valid-fork, valid-headers, headers-only, invalid)
# }
# ]
# Possible values for status:
# 1. "invalid" This branch contains at least one invalid block
# 2. "headers-only" Not all blocks for this branch are available, but the headers are valid
# 3. "valid-headers" All blocks are available for this branch, but they were never fully validated
# 4. "valid-fork" This branch is not part of the active chain, but is fully validated
# 5. "active" This is the tip of the active main chain, which is certainly valid
# 
# Examples:
# > florincoin-cli getchaintips 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getchaintips", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_chain_tips():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getchaintips","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getdifficulty
# =============
# Returns the proof-of-work difficulty as a multiple of the minimum difficulty.
# 
# Result:
# n.nnn (numeric) the proof-of-work difficulty as a multiple of the minimum difficulty.
# 
# Examples:
# > florincoin-cli getdifficulty 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getdifficulty", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_difficulty():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getdifficulty","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getmempoolinfo
# ==============
# Returns details on the active state of the TX memory pool.
# 
# Result:
# {
# "size": xxxxx (numeric) Current tx count
# "bytes": xxxxx (numeric) Sum of all tx sizes
# }
# 
# Examples:
# > florincoin-cli getmempoolinfo 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getmempoolinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_mempool_info():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getmempoolinfo","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getrawmempool ( verbose )
# =========================
# Returns all transaction ids in memory pool as a json array of string transaction ids.
# 
# Arguments:
# 1. verbose (boolean, optional, default=false) true for a json object, false for array of transaction ids
# 
# Result: (for verbose = false):
# [ (json array of string)
# "transactionid" (string) The transaction id
# ,...
# ]
# 
# Result: (for verbose = true):
# { (json object)
# "transactionid" : { (json object)
# "size" : n, (numeric) transaction size in bytes
# "fee" : n, (numeric) transaction fee in florincoins
# "time" : n, (numeric) local time transaction entered pool in seconds since 1 Jan 1970 GMT
# "height" : n, (numeric) block height when transaction entered pool
# "startingpriority" : n, (numeric) priority when transaction entered pool
# "currentpriority" : n, (numeric) transaction priority now
# "depends" : [ (array) unconfirmed transactions used as inputs for this transaction
# "transactionid", (string) parent transaction id
# ... ]
# }, ...
# ]
# 
# Examples
# > florincoin-cli getrawmempool true
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawmempool", "params": [true] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_raw_mempool(verbose=False): 
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getrawmempool","params":[' + str(verbose).lower() + ']}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# gettxout "txid" n ( includemempool )
# ====================================
# Returns details about an unspent transaction output.
# 
# Arguments:
# 1. "txid" (string, required) The transaction id
# 2. n (numeric, required) vout value
# 3. includemempool (boolean, optional) Whether to included the mem pool
# 
# Result:
# {
# "bestblock" : "hash", (string) the block hash
# "confirmations" : n, (numeric) The number of confirmations
# "value" : x.xxx, (numeric) The transaction value in flo
# "scriptPubKey" : { (json object)
# "asm" : "code", (string) 
# "hex" : "hex", (string) 
# "reqSigs" : n, (numeric) Number of required signatures
# "type" : "pubkeyhash", (string) The type, eg pubkeyhash
# "addresses" : [ (array of string) array of florincoin addresses
# "florincoinaddress" (string) florincoin address
# ,...
# ]
# },
# "version" : n, (numeric) The version
# "coinbase" : true|false (boolean) Coinbase or not
# }
# 
# Examples:
# 
# Get unspent transactions
# > florincoin-cli listunspent 
# 
# View the details
# > florincoin-cli gettxout "txid" 1
# 
# As a json rpc call
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "gettxout", "params": ["txid", 1] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_txout(txid, n, includemempool=False):
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"gettxout","params":["' + txid + '", ' + str(n) + ', ' + str(includemempool).lower() + ']}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# gettxoutsetinfo
# ===============
# Returns statistics about the unspent transaction output set.
# Note this call may take some time.
# 
# Result:
# {
# "height":n, (numeric) The current block height (index)
# "bestblock": "hex", (string) the best block hash hex
# "transactions": n, (numeric) The number of transactions
# "txouts": n, (numeric) The number of output transactions
# "bytes_serialized": n, (numeric) The serialized size
# "hash_serialized": "hash", (string) The serialized hash
# "total_amount": x.xxx (numeric) The total amount
# }
# 
# Examples:
# > florincoin-cli gettxoutsetinfo 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "gettxoutsetinfo", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_txout_set_info():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"gettxoutsetinfo","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# verifychain (checklevel, numblocks)
# ===================================
# Verifies blockchain database.
# 
# Arguments:
# 1. checklevel (numeric, optional, 0-4, default=3) How thorough the block verification is.
# 2. numblocks (numeric, optional, default=288, 0=all) The number of blocks to check.
# 
# Result:
# true|false (boolean) Verified or not
# 
# Examples:
# > florincoin-cli verifychain 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "verifychain", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def verify_chain(checklevel=3, numblocks=288):
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"verifychain","params":[' + str(checklevel) + ', ' + str(numblocks) + ']}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

## Control
# help ( "command" )
# 
# List all commands, or get help for a specified command.
# 
# Arguments:
# 1. "command" (string, optional) The command to get help on
# 
# Result:
# "text" (string) The help text
def help(command="help"):
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"help","params":["' + command + '"]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# stop
# ====
# Stop Florincoin server.
def stop():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"stop","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

## Generating
# getgenerate
# ===========
# Return if the server is set to generate coins or not. The default is false.
# It is set with the command line argument -gen (or florincoin.conf setting gen)
# It can also be set with the setgenerate call.
# 
# Result
# true|false (boolean) If the server is set to generate coins or not
# 
# Examples:
# > florincoin-cli getgenerate 
# > curl --user ${FLO_RPCUSER}:${FLO_PASSWORD} --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getgenerate", "params": [] }' -H 'content-type: text/plain;' http://127.0.0.1:7313/
def get_generate():
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"getgenerate","params":[]}'

# getinfo sub-functions
def get_balance():
    info = get_info()
    balance = info['balance']
    return balance
def get_walletversion():
    info = get_info()
    walletversion = info['walletversion']
    return walletversion
def get_version():
    info = get_info()
    version = info['version']
    return version
def get_timeoffset():
    info = get_info()
    timeoffset = info['timeoffset']
    return timeoffset
def get_testnet():
    info = get_info()
    testnet = info['testnet']
    return testnet
def get_relayfee():
    info = get_info()
    relayfee = info['relayfee']
    return relayfee
def get_proxy():
    info = get_info()
    proxy = info['proxy']
    return proxy
def get_protocolversion():
    info = get_info()
    protocolversion = info['protocolversion']
    return protocolversion
def get_paytxfee():
    info = get_info()
    paytxfee = info['paytxfee']
    return paytxfee
def get_keypoolsize():
    info = get_info()
    keypoolsize = info['keypoolsize']
    return keypoolsize
def get_keypoololdest():
    info = get_info()
    keypoololdest = info['keypoololdest']
    return keypoololdest
def get_difficulty():
    info = get_info()
    difficulty = info['difficulty']
    return difficulty
def get_connections():
    info = get_info()
    connections = info['connections']
    return connections
def get_blocks():
    info = get_info()
    blocks = info['blocks']
    return blocks
