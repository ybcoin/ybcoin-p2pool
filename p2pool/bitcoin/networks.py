import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack
from operator import *

def get_subsidy(nCap, nMaxSubsidy, bnTarget):
    bnLowerBound = 0.01
    bnUpperBound = bnSubsidyLimit = nMaxSubsidy
    bnTargetLimit = 0x00000fffff000000000000000000000000000000000000000000000000000000

    while bnLowerBound + 0.01 <= bnUpperBound:
        bnMidValue = (bnLowerBound + bnUpperBound) / 2
        if pow(bnMidValue, nCap) * bnTargetLimit > pow(bnSubsidyLimit, nCap) * bnTarget:
            bnUpperBound = bnMidValue
        else:
            bnLowerBound = bnMidValue

    nSubsidy = round(bnMidValue, 2)

    if nSubsidy > bnMidValue:
        nSubsidy = nSubsidy - 0.01

    return int(nSubsidy * 1000000)

def debug_block_info(dat1):
	print 'block header',  data.block_header_type.unpack(dat1)['timestamp']
	return 0

nets = dict(
    ybcoin=math.Object(
        P2P_PREFIX='d4e7e8e5'.decode('hex'),
        P2P_PORT=7337,
        ADDRESS_VERSION=78,
        RPC_PORT=8344,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'ybcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(6, 10, target),
        BLOCKHASH_FUNC=lambda header: pack.IntType(256).unpack(__import__('ybc_scrypt').getPoWHash(header, data.block_header_type.unpack(header)['timestamp'])),
        POW_FUNC=lambda header: pack.IntType(256).unpack(__import__('ybc_scrypt').getPoWHash(header, data.block_header_type.unpack(header)['timestamp'])),
        BLOCK_PERIOD=60, # s
        SYMBOL='YBC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'ybcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/ybcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.ybcoin'), 'ybcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://ybcexplorer.tk/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://ybcexplorer.tk/address/',
        SANE_TARGET_RANGE=(2**256//2**20//1000 - 1, 2**256//2**20 - 1),
    ),

    ybcoin_testnet=math.Object(
        P2P_PREFIX='d4e7e8e5'.decode('hex'),
        P2P_PORT=7337,
        ADDRESS_VERSION=78,
        RPC_PORT=8344,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'ybcoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(6, 10, target),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('ybc_scrypt').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ybc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='YBC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'YbCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/YbCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.ybcoin'), 'ybcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://nonexistent-ybcoin-testnet-explorer/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://nonexistent-ybcoin-testnet-explorer/address/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
