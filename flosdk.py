## Connect to FLO RPC
## Send an appdata message using a library function
## This requires a connection to a local running FLO node
# Special thanks: MustyMouse
# Special thanks: technanner

import requests 
import os
import pprint
import traceback

## TODO: Versioning 

## Library functions
# Get info from FLO RPC using getinfo call 
# This function is the basis for all getinfo sub-functions
def get_info():
    payload = b'{"jsonrpc":"1.0","id":"curltext","method":"getinfo","params":[]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), 
            data=payload,
            headers=headers,
            auth=(os.environ['FLO_RPCUSER'],
            os.environ['FLO_PASSWORD'])
    )
    return r.json()

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
    print address
    # TODO: figure out str.format() instead of concat
    payload = '{"jsonrpc":"1.0","id":"curltext","method":"sendtoaddress","params":["' + address + '", 0.1, "", "", "' + appdata + '"]}'
    headers = {'content-type': 'text/plain'}
    r = requests.post('http://localhost:{}'.format(os.environ['FLO_RPCPORT']), data=payload, headers=headers, auth=(os.environ['FLO_RPCUSER'], os.environ['FLO_PASSWORD']))
    if r.json()['error'] is not None:
        raise Exception(r.json()['error'])
    else:
        return r.json()['result']

# getinfo sub-functions
def get_balance():
    info = get_info()
    balance = info['result']['balance']
    return balance
def get_walletversion():
    info = get_info()
    walletversion = info['result']['walletversion']
    return walletversion
def get_version():
    info = get_info()
    version = info['result']['version']
    return version
def get_timeoffset():
    info = get_info()
    timeoffset = info['result']['timeoffset']
    return timeoffset
def get_testnet():
    info = get_info()
    testnet = info['result']['testnet']
    return testnet
def get_relayfee():
    info = get_info()
    relayfee = info['result']['relayfee']
    return relayfee
def get_proxy():
    info = get_info()
    proxy = info['result']['proxy']
    return proxy
def get_protocolversion():
    info = get_info()
    protocolversion = info['result']['protocolversion']
    return protocolversion
def get_paytxfee():
    info = get_info()
    paytxfee = info['result']['paytxfee']
    return paytxfee
def get_keypoolsize():
    info = get_info()
    keypoolsize = info['result']['keypoolsize']
    return keypoolsize
def get_keypoololdest():
    info = get_info()
    keypoololdest = info['result']['keypoololdest']
    return keypoololdest
def get_difficulty():
    info = get_info()
    difficulty = info['result']['difficulty']
    return difficulty
def get_connections():
    info = get_info()
    connections = info['result']['connections']
    return connections
def get_blocks():
    info = get_info()
    blocks = info['result']['blocks']
    return blocks

## testing
print "Getinfo:"
pprint.pprint(get_info())
print "Wallet version: {}".format(get_walletversion())
print "Time offset: {}".format(get_timeoffset())
print "Testnet: {}".format(get_testnet())
print "Relay fee: {}".format(get_relayfee())
print "Proxy: {}".format(get_proxy())
print "Protocolversion: {}".format(get_protocolversion())
print "Balance: {} FLO".format(get_balance())
print "Blocks: {}".format(get_blocks())
print "Difficulty: {}".format(get_difficulty())
print "Keypoolsize: {}".format(get_keypoolsize())
print "Keypooldest: {}".format(get_keypoololdest())
print "Paytxfee: {}".format(get_paytxfee())

account = ""
try:
    address = get_account_address(account)
    print "Get account address: {}".format(address)
except Exception as (e):
    # TODO: Create FLORPCException
    print "Failed to get account address:"
    print traceback.print_exc(e)

appdata = "Hello world!"
print "Write to blockchain: "
try:
    print write_to_blockchain(address, appdata)
except Exception as (e):
    # TODO: Create FLORPCException
    print "Failed to write to blockchain:"
    print e
    print traceback.print_exc(e)
    
## connection interface?
